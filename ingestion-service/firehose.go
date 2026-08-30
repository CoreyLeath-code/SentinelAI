package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/firehose"
	"github.com/aws/aws-sdk-go-v2/service/firehose/types"
	"github.com/prometheus/client_golang/prometheus"
)

const (
	defaultFirehoseQueueSize = 1000
	firehosePublishTimeout   = 5 * time.Second
)

var firehoseRecordsTotal = prometheus.NewCounterVec(
	prometheus.CounterOpts{
		Name: "ingestion_firehose_records_total",
		Help: "Inference telemetry records handled by the optional Amazon Data Firehose mirror.",
	},
	[]string{"status"},
)

func init() {
	prometheus.MustRegister(firehoseRecordsTotal)
}

type firehoseAPI interface {
	PutRecord(context.Context, *firehose.PutRecordInput, ...func(*firehose.Options)) (*firehose.PutRecordOutput, error)
}

type firehosePublisher struct {
	client     firehoseAPI
	streamName string
}

type firehoseDispatcher struct {
	publisher *firehosePublisher
	queue     chan InferenceLog
}

func newFirehoseDispatcher() (*firehoseDispatcher, error) {
	if !strings.EqualFold(strings.TrimSpace(os.Getenv("FIREHOSE_ENABLED")), "true") {
		return nil, nil
	}

	streamName := strings.TrimSpace(os.Getenv("FIREHOSE_DELIVERY_STREAM"))
	if streamName == "" {
		return nil, errors.New("FIREHOSE_DELIVERY_STREAM is required when FIREHOSE_ENABLED=true")
	}

	region := strings.TrimSpace(os.Getenv("AWS_REGION"))
	if region == "" {
		region = "us-east-1"
	}

	queueSize := defaultFirehoseQueueSize
	if raw := strings.TrimSpace(os.Getenv("FIREHOSE_QUEUE_SIZE")); raw != "" {
		parsed, err := strconv.Atoi(raw)
		if err != nil || parsed < 1 {
			return nil, fmt.Errorf("FIREHOSE_QUEUE_SIZE must be a positive integer: %q", raw)
		}
		queueSize = parsed
	}

	cfg, err := config.LoadDefaultConfig(context.Background(), config.WithRegion(region))
	if err != nil {
		return nil, fmt.Errorf("load AWS configuration: %w", err)
	}

	dispatcher := &firehoseDispatcher{
		publisher: &firehosePublisher{
			client:     firehose.NewFromConfig(cfg),
			streamName: streamName,
		},
		queue: make(chan InferenceLog, queueSize),
	}
	go dispatcher.run()

	return dispatcher, nil
}

func (d *firehoseDispatcher) enqueue(entry InferenceLog) {
	select {
	case d.queue <- entry:
		firehoseRecordsTotal.WithLabelValues("queued").Inc()
	default:
		firehoseRecordsTotal.WithLabelValues("dropped").Inc()
		log.Printf("firehose mirror queue full; dropping telemetry record for model=%s", entry.ModelID)
	}
}

func (d *firehoseDispatcher) run() {
	for entry := range d.queue {
		ctx, cancel := context.WithTimeout(context.Background(), firehosePublishTimeout)
		err := d.publisher.publish(ctx, entry)
		cancel()

		if err != nil {
			firehoseRecordsTotal.WithLabelValues("error").Inc()
			log.Printf("firehose PutRecord failed for model=%s: %v", entry.ModelID, err)
			continue
		}
		firehoseRecordsTotal.WithLabelValues("delivered").Inc()
	}
}

func (p *firehosePublisher) publish(ctx context.Context, entry InferenceLog) error {
	payload, err := encodeFirehoseRecord(entry)
	if err != nil {
		return err
	}

	_, err = p.client.PutRecord(ctx, &firehose.PutRecordInput{
		DeliveryStreamName: &p.streamName,
		Record: &types.Record{
			Data: payload,
		},
	})
	if err != nil {
		return fmt.Errorf("put record: %w", err)
	}
	return nil
}

func encodeFirehoseRecord(entry InferenceLog) ([]byte, error) {
	payload, err := json.Marshal(entry)
	if err != nil {
		return nil, fmt.Errorf("marshal inference log: %w", err)
	}

	// Firehose concatenates records inside delivered objects. NDJSON keeps each
	// inference event independently parseable after buffering and compression.
	return append(payload, '\n'), nil
}
