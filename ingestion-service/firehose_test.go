package main

import (
	"context"
	"encoding/json"
	"testing"
	"time"

	"github.com/aws/aws-sdk-go-v2/service/firehose"
)

type stubFirehoseClient struct {
	input *firehose.PutRecordInput
}

func (s *stubFirehoseClient) PutRecord(_ context.Context, input *firehose.PutRecordInput, _ ...func(*firehose.Options)) (*firehose.PutRecordOutput, error) {
	s.input = input
	recordID := "test-record"
	return &firehose.PutRecordOutput{RecordId: &recordID}, nil
}

func TestNewFirehoseDispatcherDisabledByDefault(t *testing.T) {
	t.Setenv("FIREHOSE_ENABLED", "false")

	dispatcher, err := newFirehoseDispatcher()
	if err != nil {
		t.Fatalf("newFirehoseDispatcher returned error: %v", err)
	}
	if dispatcher != nil {
		t.Fatal("dispatcher should be nil when Firehose is disabled")
	}
}

func TestNewFirehoseDispatcherRequiresStream(t *testing.T) {
	t.Setenv("FIREHOSE_ENABLED", "true")
	t.Setenv("FIREHOSE_DELIVERY_STREAM", "")

	if _, err := newFirehoseDispatcher(); err == nil {
		t.Fatal("expected missing stream configuration to return an error")
	}
}

func TestFirehosePublisherUsesNDJSON(t *testing.T) {
	client := &stubFirehoseClient{}
	publisher := &firehosePublisher{client: client, streamName: "sentinelai-telemetry"}
	entry := InferenceLog{
		ModelID:      "demo",
		ModelVersion: "v1",
		LatencyMs:    42,
		Status:       "ok",
		Timestamp:    time.Date(2026, 8, 30, 18, 0, 0, 0, time.UTC),
	}

	if err := publisher.publish(context.Background(), entry); err != nil {
		t.Fatalf("publish returned error: %v", err)
	}
	if client.input == nil || client.input.Record == nil {
		t.Fatal("PutRecord input was not captured")
	}
	if got := *client.input.DeliveryStreamName; got != "sentinelai-telemetry" {
		t.Fatalf("stream name = %q, want sentinelai-telemetry", got)
	}

	payload := client.input.Record.Data
	if len(payload) == 0 || payload[len(payload)-1] != '\n' {
		t.Fatalf("payload must be newline-delimited JSON: %q", payload)
	}

	var decoded InferenceLog
	if err := json.Unmarshal(payload[:len(payload)-1], &decoded); err != nil {
		t.Fatalf("payload is not valid JSON: %v", err)
	}
	if decoded.ModelID != entry.ModelID || decoded.LatencyMs != entry.LatencyMs {
		t.Fatalf("decoded payload = %#v, want model=%q latency=%d", decoded, entry.ModelID, entry.LatencyMs)
	}
}
