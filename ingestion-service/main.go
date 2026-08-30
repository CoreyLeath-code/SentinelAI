// ingestion-service/main.go — SentinelAI inference-log ingestion endpoint.
//
// Environment variables:
//   DATABASE_URL              — Postgres DSN (required when WAREHOUSE_MODE=postgres)
//   WAREHOUSE_MODE            — "postgres" (default) | "snowflake"
//   FIREHOSE_ENABLED          — mirror accepted telemetry to Amazon Data Firehose when true
//   FIREHOSE_DELIVERY_STREAM  — Firehose stream name (required when enabled)
//   FIREHOSE_QUEUE_SIZE       — bounded in-memory mirror queue size (default 1000)
//   AWS_REGION                — AWS region for Firehose (default us-east-1)
//   PORT                      — listen port (default 8080)
package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"time"

	_ "github.com/lib/pq"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

// ---------------------------------------------------------------------------
// Metrics
// ---------------------------------------------------------------------------

var (
	ingestTotal = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Name: "ingestion_logs_total",
			Help: "Total inference logs received.",
		},
		[]string{"status"},
	)
	ingestLatency = prometheus.NewHistogram(prometheus.HistogramOpts{
		Name:    "ingestion_handler_seconds",
		Help:    "Handler latency in seconds.",
		Buckets: prometheus.DefBuckets,
	})
)

func init() {
	prometheus.MustRegister(ingestTotal, ingestLatency)
}

// ---------------------------------------------------------------------------
// Request / response types
// ---------------------------------------------------------------------------

type InferenceLog struct {
	ModelID      string                 `json:"model_id"`
	ModelVersion string                 `json:"model_version,omitempty"`
	LatencyMs    int                    `json:"latency_ms"`
	TokensIn     int                    `json:"tokens_in,omitempty"`
	TokensOut    int                    `json:"tokens_out,omitempty"`
	Status       string                 `json:"status,omitempty"`
	Features     map[string]interface{} `json:"features,omitempty"`
	Timestamp    time.Time              `json:"timestamp,omitempty"`
}

// ---------------------------------------------------------------------------
// Globals
// ---------------------------------------------------------------------------

var db *sql.DB
var firehoseMirror *firehoseDispatcher

// ---------------------------------------------------------------------------
// Handlers
// ---------------------------------------------------------------------------

// healthHandler reports process liveness. It intentionally does not depend on
// Postgres so an orchestrator can distinguish a failed dependency from a dead process.
func healthHandler(w http.ResponseWriter, _ *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "ok", "service": "ingestion-service"})
}

// readyHandler reports whether this replica can accept durable ingestion writes.
// Firehose is an optional fail-open telemetry mirror, so its health is exposed by
// metrics/logs rather than making the primary ingestion readiness depend on AWS.
func readyHandler(w http.ResponseWriter, _ *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	if db != nil {
		if err := db.Ping(); err != nil {
			w.WriteHeader(http.StatusServiceUnavailable)
			json.NewEncoder(w).Encode(map[string]string{"status": "degraded", "error": err.Error()})
			return
		}
	}
	json.NewEncoder(w).Encode(map[string]string{"status": "ok", "service": "ingestion-service"})
}

func withOptionalInstanceID(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// This header is disabled in normal operation. It is a deterministic
		// test aid for the Compose scaling smoke test, not a public identifier.
		if os.Getenv("EXPOSE_INSTANCE_ID") == "true" {
			instanceID := os.Getenv("INSTANCE_ID")
			if instanceID == "" {
				instanceID, _ = os.Hostname()
			}
			if instanceID != "" {
				w.Header().Set("X-Instance-ID", instanceID)
			}
		}
		next.ServeHTTP(w, r)
	})
}

func newMux() *http.ServeMux {
	mux := http.NewServeMux()
	mux.Handle("/log", withOptionalInstanceID(http.HandlerFunc(logHandler)))
	mux.Handle("/health", withOptionalInstanceID(http.HandlerFunc(healthHandler)))
	mux.Handle("/ready", withOptionalInstanceID(http.HandlerFunc(readyHandler)))
	mux.Handle("/metrics", withOptionalInstanceID(promhttp.Handler()))
	return mux
}

func logHandler(w http.ResponseWriter, r *http.Request) {
	timer := prometheus.NewTimer(ingestLatency)
	defer timer.ObserveDuration()

	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var entry InferenceLog
	if err := json.NewDecoder(r.Body).Decode(&entry); err != nil {
		ingestTotal.WithLabelValues("error").Inc()
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if entry.Status == "" {
		entry.Status = "ok"
	}
	if entry.Timestamp.IsZero() {
		entry.Timestamp = time.Now().UTC()
	}

	warehouseMode := os.Getenv("WAREHOUSE_MODE")
	if warehouseMode == "" {
		warehouseMode = "postgres"
	}

	if warehouseMode == "postgres" && db != nil {
		featuresJSON, _ := json.Marshal(entry.Features)
		_, err := db.Exec(`
			INSERT INTO inference_logs
			  (model_id, model_version, latency_ms, tokens_in, tokens_out, status, features, created_at)
			VALUES ($1,$2,$3,$4,$5,$6,$7,$8)`,
			entry.ModelID, entry.ModelVersion, entry.LatencyMs,
			entry.TokensIn, entry.TokensOut, entry.Status,
			string(featuresJSON), entry.Timestamp,
		)
		if err != nil {
			log.Printf("db insert error: %v", err)
			ingestTotal.WithLabelValues("db_error").Inc()
			http.Error(w, "database error", http.StatusInternalServerError)
			return
		}
	} else {
		// Snowflake or no DB — just log for now.
		log.Printf("[%s] model=%s latency=%dms status=%s",
			warehouseMode, entry.ModelID, entry.LatencyMs, entry.Status)
	}

	// The AWS path is intentionally a non-blocking mirror. Queue pressure or a
	// transient Firehose failure is visible in metrics and logs but does not turn
	// telemetry delivery into a failure of the primary ingestion request.
	if firehoseMirror != nil {
		firehoseMirror.enqueue(entry)
	}

	ingestTotal.WithLabelValues("ok").Inc()
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusAccepted)
	json.NewEncoder(w).Encode(map[string]string{"status": "accepted"})
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

func main() {
	warehouseMode := os.Getenv("WAREHOUSE_MODE")
	if warehouseMode == "" {
		warehouseMode = "postgres"
	}

	if warehouseMode == "postgres" {
		dsn := os.Getenv("DATABASE_URL")
		if dsn == "" {
			dsn = "postgres://sentinel:sentinel@postgres:5432/sentinel?sslmode=disable"
		}
		var err error
		for i := 0; i < 10; i++ {
			db, err = sql.Open("postgres", dsn)
			if err == nil {
				if err = db.Ping(); err == nil {
					break
				}
			}
			log.Printf("waiting for postgres (%d/10): %v", i+1, err)
			time.Sleep(3 * time.Second)
		}
		if err != nil {
			log.Fatalf("could not connect to postgres: %v", err)
		}
		log.Println("connected to postgres")
	}

	var err error
	firehoseMirror, err = newFirehoseDispatcher()
	if err != nil {
		log.Fatalf("could not configure Firehose mirror: %v", err)
	}
	if firehoseMirror != nil {
		log.Printf("Amazon Data Firehose mirror enabled (stream=%s)", firehoseMirror.publisher.streamName)
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("SentinelAI Ingestion Service running on :%s (warehouse=%s)", port, warehouseMode)
	log.Fatal(http.ListenAndServe(":"+port, newMux()))
}
