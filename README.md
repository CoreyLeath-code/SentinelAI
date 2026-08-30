<p align="center">
  <img width="960" alt="SentinelAI interface" src="https://github.com/user-attachments/assets/33e7a5fb-be0a-495b-a950-7a14b9aedb4b" />
</p>

# SentinelAI — Reproducible Drift-Monitoring Reference System

<p align="center">
  <a href="https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/ci-cd.yml"><img alt="CI" src="https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/ci-cd.yml/badge.svg" /></a>
  <a href="https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/aws-telemetry.yml"><img alt="AWS telemetry CI" src="https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/aws-telemetry.yml/badge.svg" /></a>
  <a href="https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/benchmarks.yml"><img alt="Research benchmark" src="https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/benchmarks.yml/badge.svg" /></a>
  <a href="https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/security.yml"><img alt="Security" src="https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/security.yml/badge.svg" /></a>
  <a href="https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/sast.yml"><img alt="SAST" src="https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/sast.yml/badge.svg" /></a>
  <a href="https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/data-validation.yml"><img alt="Schema validation" src="https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/data-validation.yml/badge.svg" /></a>
</p>

<p align="center">
  <a href="docs/aws-firehose-s3.md"><img alt="AWS Data Firehose and S3" src="https://img.shields.io/badge/AWS-Data%20Firehose%20%2B%20S3-FF9900?logo=amazonwebservices&amp;logoColor=white" /></a>
  <a href="benchmarks/benchmark_report.md"><img alt="Python reference p95" src="https://img.shields.io/badge/Python_reference_p95-54.7_%C2%B5s-6f42c1" /></a>
  <a href="benchmarks/benchmark_report.md"><img alt="Synthetic decision F1" src="https://img.shields.io/badge/synthetic_decision_F1-1.000-2ea44f" /></a>
  <a href="LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" /></a>
</p>

## Abstract

SentinelAI is a multi-service observability prototype for AI systems. Its directly implemented statistical component compares an expected and an observed histogram with Population Stability Index (PSI) and a Kolmogorov–Smirnov (KS) CDF distance, then raises a drift flag when either configured threshold is crossed.

The Go ingestion service can optionally mirror accepted inference telemetry to Amazon Data Firehose, which Terraform configures to deliver GZIP-compressed NDJSON objects into a private, versioned, encrypted Amazon S3 telemetry bucket. This AWS path is disabled by default for local development and is a best-effort observability mirror, not a transactional dual-write guarantee.

The versioned evidence measures a portable Python reference of the drift decision rule on seeded 32-bin synthetic histograms—not native C++ execution, HTTP latency, concurrent service load, Firehose/S3 throughput, or production drift-detection accuracy. The benchmark is a repeatable regression signal, not a claim of real-world model quality.

## Formal decision rule

Let $p=(p_1,...,p_B)$ and $q=(q_1,...,q_B)$ be expected and actual histogram-bin weights. The C++ engine computes

\[
\operatorname{PSI}(p,q) = \sum_{i=1}^{B}(q_i-p_i)\log\left(\frac{q_i}{p_i}\right),
\]

summing only bins where both values are positive. It also forms normalized cumulative distributions:

\[
P_k=\sum_{i=1}^{k}\frac{p_i}{\sum_jp_j},\qquad Q_k=\sum_{i=1}^{k}\frac{q_i}{\sum_jq_j},\qquad \operatorname{KS}(p,q)=\max_{1\leq k\leq B}|P_k-Q_k|.
\]

The implementation emits a drift event when

\[
\operatorname{drift}(p,q)=[\operatorname{PSI}(p,q)>0.20]\lor[\operatorname{KS}(p,q)>0.10].
\]

This logic is implemented in [drift-engine/drift_engine.cpp](drift-engine/drift_engine.cpp) and mirrored by [benchmarks/run_benchmark.py](benchmarks/run_benchmark.py). The benchmark supplies normalized positive bins; the service does not add smoothing to zero-valued PSI bins, so zero handling is an explicit limitation of the present implementation.

For $B$ bins, PSI and KS each make one linear pass: $O(B)$ time and $O(1)$ auxiliary working memory (apart from the input vectors). The calculation is not a hypothesis test: the two thresholds are fixed decision settings, not calibrated p-values.

## Evidence snapshot

| Measured quantity | Value | What it measures |
|---|---:|---|
| Timed reference evaluations | 20,000 | Seeded, single-process Python decision evaluations after 100 warm-ups |
| Reference latency (median / p95 / p99) | 39.700 / 54.700 / 76.200 µs | Per-decision Python reference latency |
| Reference throughput | 23,031.13 operations/s | Same Python reference workload |
| Peak traced memory | 0.623 MiB | Python allocations reported by tracemalloc |
| Synthetic decision precision / recall / F1 | 1.000 / 1.000 / 1.000 | 2,000 deliberately separated seeded perturbation cases |
| Decision thresholds | PSI > 0.20 or KS > 0.10 | Thresholds hard-coded by the C++ reference implementation |

The full protocol, environment (CPython 3.12.13 on Windows 11), raw confusion matrix, and limitations are versioned in [benchmarks/latest.json](benchmarks/latest.json) and explained in [benchmarks/benchmark_report.md](benchmarks/benchmark_report.md). Reproduce the artifact with:

```bash
python benchmarks/run_benchmark.py --output benchmarks/latest.json
```

## Research questions

1. Under a leakage-free, labeled production dataset, how well do the fixed PSI/KS thresholds detect meaningful distribution shift?
2. How sensitive are false positives and false negatives to bin count, threshold selection, and zero-bin handling?
3. How does native C++ and end-to-end service latency scale with histogram size and concurrent requests?
4. Which operational metrics best distinguish feature drift from changes in data volume or service latency?

## Production Readiness Guide

> This section is the portfolio audit entry point for **SentinelAI**. It describes an engineering promotion path; it is not a claim that the repository is already production-authorized.

### Architecture flowchart

```mermaid
flowchart LR
    Source --> Build[Release binary] --> Tests[Unit + sanitizer tests] --> Artifact[Versioned artifact]
```

### Quickstart and local validation

The repository uses Python services, a Go ingestion service, and a small C++ drift executable. Reproduce the portable evidence or build the statistical engine directly:

```bash
python benchmarks/run_benchmark.py --output benchmarks/latest.json
g++ -std=c++17 drift-engine/drift_engine.cpp -o drift-engine/drift_engine
```

If the project uses external services, model artifacts, cloud credentials, or private data, start them through documented local fixtures or mocks. Never place secrets or identifiable records in the repository.

### Research-style metrics and benchmarks

| Evidence | Required record |
|---|---|
| Correctness | Test command, commit SHA, runtime, and pass/fail result |
| Performance | Warm-up, sample count, concurrency, median, p95, p99, throughput, and memory |
| Data/model quality | Dataset version, split strategy, leakage controls, calibration, subgroup results, and uncertainty |
| Runtime | Image digest, health-check latency, resource limits, and rollback target |
| Security | Dependency, secret, SAST, container, and SBOM results |

A benchmark number belongs in a versioned artifact tied to a commit and hardware/runtime description. Engineering benchmarks must not be presented as clinical, financial, safety, or model-quality validation without the appropriate domain evidence.

### Extended Q&A

**What is production-ready for this repository?**  
A reproducible build, tested public contract, controlled configuration, observable runtime, documented security boundary, versioned artifacts, and a tested rollback path.

**What must remain explicit?**  
The intended use, excluded use, data/credential handling, model or algorithm limitations, and which metrics are measured versus aspirational.

**What should be completed next?**  
Use the linked production-readiness issue for this repository as the checklist. Resolve missing tests, deployment instructions, observability, supply-chain controls, and release evidence before attaching a production claim.

## 🏛️ Advanced Platform Architecture & Telemetry Decoupling

SentinelAI separates primary inference paths from telemetry and evaluation layers in its local architecture.

```text
[ Incoming User Query ] ───► [ Async Proxy Gateway ] ───► [ Downstream Application ]
                                      │
                         (Non-Blocking Telemetry Mirror)
                                      ▼
                    ┌──────────────────────────────────────┐
                    │    SentinelAI Asynchronous Engine    │
                    ├──────────────────────────────────────┤
                    │  • Parallelized Guardrail Evaluation │
                    │  • LLM SRE Diagnostics               │
                    │  • Token Cost & Allocation Trackers  │
                    └──────────────────┬───────────────────┘
                                       ▼
                         [ Streamlit Observability Control Plane ]
```

## 🚀 Quickstart — Docker Compose (recommended)

> **Prerequisites:** Docker 24+ with Compose v2 (`docker compose version`).

```bash
# 1. Copy environment defaults
cp .env.example .env

# 2. Start the full local stack
docker compose up --build
```

Once running, open:

| Service | URL |
|---------|-----|
| Streamlit Dashboard | http://localhost:8501 |
| Prometheus | http://localhost:9090 |
| Grafana (admin / admin) | http://localhost:3000 |
| Ingestion API (NGINX gateway) | http://localhost:8080 |
| Drift Engine API | http://localhost:7070 |
| LLM Guard API | http://localhost:8000 |

### Send a sample inference log

```bash
curl -X POST http://localhost:8080/log \
  -H "Content-Type: application/json" \
  -d '{"model_id":"demo","model_version":"v1","latency_ms":120,"tokens_in":32,"tokens_out":64,"status":"ok"}'
```

### Run a drift computation

```bash
curl -X POST http://localhost:7070/drift \
  -H "Content-Type: application/json" \
  -d '{"model_id":"demo","feature_name":"latency","expected":[0.2,0.3,0.25,0.25],"actual":[0.1,0.35,0.30,0.25]}'
```

### Summarize an incident (Ollama optional — falls back to rule-based stub)

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"log_data":"PSI 0.35 on latency feature, model demo v1","persist":false}'
```

---

## ⚙️ Configuration

All configuration is via environment variables. Copy `.env.example` to `.env` and adjust.

| Variable | Default | Description |
|----------|---------|-------------|
| `WAREHOUSE_MODE` | `postgres` | `postgres` (local) or `snowflake` |
| `DATABASE_URL` | Postgres DSN | Full Postgres connection string |
| `POSTGRES_USER` | `sentinel` | Postgres user |
| `POSTGRES_PASSWORD` | `sentinel` | Postgres password |
| `POSTGRES_DB` | `sentinel` | Postgres database |
| `FIREHOSE_ENABLED` | `false` | Enables the optional non-blocking Amazon Data Firehose telemetry mirror |
| `FIREHOSE_DELIVERY_STREAM` | `sentinelai-telemetry` | Firehose delivery stream name |
| `FIREHOSE_QUEUE_SIZE` | `1000` | Maximum in-memory records waiting for Firehose delivery |
| `AWS_REGION` | `us-east-1` | AWS region used by the Firehose client |
| `OLLAMA_HOST` | `http://ollama:11434` | Ollama endpoint (optional) |
| `LLM_MODEL` | `llama2` | LLM model name |
| `API_BEARER_TOKEN` | *(unset)* | Required shared bearer token for `POST /infer`; the endpoint returns 503 until configured |

**Snowflake (optional):** set `WAREHOUSE_MODE=snowflake` and fill in `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`, `SNOWFLAKE_WAREHOUSE`.

---

## Load-balanced ingestion path

The host-facing ingestion endpoint is an NGINX gateway at port `8080`; Go ingestion replicas are internal-only and can be started with `docker compose up --build --scale ingestion-service=3`. `/health` is liveness and `/ready` includes the Postgres dependency; the CI smoke test checks gateway readiness, multi-replica routing, and continued readiness after one replica stops. The optional `EXPOSE_INSTANCE_ID=true` setting exists only for that test and is disabled by default.

When `FIREHOSE_ENABLED=true`, a bounded worker mirrors accepted inference events to Amazon Data Firehose after the primary warehouse path succeeds. Firehose queue pressure or AWS delivery errors do not change `/ready` and do not fail an otherwise accepted primary ingestion request; they are surfaced through Prometheus metrics and logs.

## 🏗️ Architecture

```text
User → NGINX Ingestion Gateway (8080) → Go Ingestion Replicas → Postgres (local) / Snowflake (optional)
                                        │
                                        ├──► bounded Firehose queue ──► Amazon Data Firehose ──► Amazon S3
                                        │                                  │
                                        │                                  └──► CloudWatch delivery logs
                                        ↓
                              Drift Engine C++ (7070)
                                        ↓
                               LLM Guard Python (8000)
                                        ↓
                           Streamlit Dashboard (8501)
                                        ↓
                         Prometheus (9090) + Grafana (3000)
```

### Services

| Service | Language | Port | Description |
|---------|----------|------|-------------|
| `ingestion-service` | Go | 8080 | Receives inference logs, writes to warehouse, optionally mirrors to Firehose |
| `drift-engine` | C++ + Python | 7070 | PSI/KS drift detection |
| `llm-guard` | Python | 8000 | LLM-powered incident summarization |
| `streamlit-dashboard` | Python | 8501 | Control plane UI |
| `postgres` | — | 5432 | Local warehouse (default) |
| `prometheus` | — | 9090 | Metrics scraping |
| `grafana` | — | 3000 | Dashboards |
| Amazon Data Firehose | AWS managed | — | Optional telemetry buffering and delivery |
| Amazon S3 | AWS managed | — | Optional compressed telemetry lake |

---

## ☁️ AWS telemetry mirror — Amazon Data Firehose + S3

The `terraform/` configuration defines an AWS telemetry path that can be provisioned independently of local Docker Compose:

```mermaid
flowchart LR
    App[Model / application] --> Gateway[NGINX]
    Gateway --> Go[Go ingestion replicas]
    Go --> Warehouse[(Postgres / Snowflake path)]
    Go -. bounded fail-open mirror .-> Queue[In-memory queue]
    Queue --> Firehose[Amazon Data Firehose]
    Firehose --> S3[(Private S3 telemetry bucket)]
    Firehose --> CW[CloudWatch delivery logs]
```

Terraform defines a private S3 bucket with public-access blocking, versioning, SSE-S3 encryption and a configurable retention policy; a Firehose stream with 60-second / 5-MiB buffering, GZIP compression and time-partitioned S3 prefixes; CloudWatch delivery logging; a Firehose service role; and a separate least-privilege writer policy for the SentinelAI workload.

```bash
cd terraform
terraform init
terraform fmt -check
terraform validate
terraform plan
```

Do not commit AWS access keys. The Go producer uses the AWS SDK default credential chain; for an EKS deployment, attach the Terraform `firehose_writer_policy_arn` output to the ingestion workload identity rather than injecting long-lived credentials.

Producer-side observability is exposed through:

```text
ingestion_firehose_records_total{status="queued"}
ingestion_firehose_records_total{status="delivered"}
ingestion_firehose_records_total{status="error"}
ingestion_firehose_records_total{status="dropped"}
```

### AWS validation boundary

The repository CI validates the AWS integration code without requiring AWS credentials:

- `go mod tidy` must produce no module-file drift.
- `go test ./...` validates Firehose configuration and NDJSON `PutRecord` behavior against a fake client.
- `terraform fmt`, `terraform init -backend=false`, and `terraform validate` verify the IaC syntax and provider graph.
- The normal Docker Compose CI continues to exercise the local multi-replica ingestion path with Firehose disabled by default.

CI does **not** run `terraform apply`, create billable AWS resources, or prove live Firehose-to-S3 delivery. Live AWS throughput, durability, retry behavior, IAM attachment, and end-to-end delivery latency remain deployment-level validation work.

This path is implemented as a best-effort telemetry mirror. The queue is bounded and in-memory, process termination can lose queued mirror records, and SDK retries may create duplicates. See [docs/aws-firehose-s3.md](docs/aws-firehose-s3.md) for deployment, IAM, failure semantics, observability, and cost controls.

---

## 📊 Research Metrics & Benchmarks

The committed baseline is generated by a seeded, dependency-free harness that mirrors the PSI/KS decision rule in the C++ drift engine. These numbers measure the Python reference implementation—not native C++ or end-to-end HTTP latency. See the [full methodology, interpretation, and limitations](benchmarks/benchmark_report.md) and [raw JSON evidence](benchmarks/latest.json).

### Latest reproducible baseline

| Metric | Value | Protocol | Source |
|---|---:|---|---|
| Timed evaluations | 20,000 | 100 warm-ups, 32 bins, seed `20260718` | `python benchmarks/run_benchmark.py --iterations 20000 --evaluation-samples 2000 --output benchmarks/latest.json`; `benchmarks/run_benchmark.py` → `benchmarks/latest.json` |
| Mean latency | 41.706 µs | Per-decision reference latency | `python benchmarks/run_benchmark.py --iterations 20000 --evaluation-samples 2000 --output benchmarks/latest.json`; `benchmarks/run_benchmark.py` → `benchmarks/latest.json` |
| Median latency | 39.700 µs | Per-decision reference latency | `python benchmarks/run_benchmark.py --iterations 20000 --evaluation-samples 2000 --output benchmarks/latest.json`; `benchmarks/run_benchmark.py` → `benchmarks/latest.json` |
| P95 / P99 latency | 54.700 / 76.200 µs | Linear percentile interpolation | `python benchmarks/run_benchmark.py --iterations 20000 --evaluation-samples 2000 --output benchmarks/latest.json`; `benchmarks/run_benchmark.py` → `benchmarks/latest.json` |
| Minimum / maximum | 23.700 / 319.200 µs | Observed range | `python benchmarks/run_benchmark.py --iterations 20000 --evaluation-samples 2000 --output benchmarks/latest.json`; `benchmarks/run_benchmark.py` → `benchmarks/latest.json` |
| Throughput | 23,031.13 operations/s | Single-process CPython reference | `python benchmarks/run_benchmark.py --iterations 20000 --evaluation-samples 2000 --output benchmarks/latest.json`; `benchmarks/run_benchmark.py` → `benchmarks/latest.json` |
| Peak traced memory | 0.623 MiB | Python `tracemalloc` | `python benchmarks/run_benchmark.py --iterations 20000 --evaluation-samples 2000 --output benchmarks/latest.json`; `benchmarks/run_benchmark.py` → `benchmarks/latest.json` |
| Precision / recall / F1 | 1.000 / 1.000 / 1.000 | 2,000 balanced synthetic cases | `python benchmarks/run_benchmark.py --iterations 20000 --evaluation-samples 2000 --output benchmarks/latest.json`; `benchmarks/run_benchmark.py` → `benchmarks/latest.json` |
| Confusion matrix | TP 1000 · TN 1000 · FP 0 · FN 0 | Controlled seeded classes | `python benchmarks/run_benchmark.py --iterations 20000 --evaluation-samples 2000 --output benchmarks/latest.json`; `benchmarks/run_benchmark.py` → `benchmarks/latest.json` |
| Environment | CPython 3.12.13 · Windows 11 | Recorded 2026-07-18 | `python benchmarks/run_benchmark.py --iterations 20000 --evaluation-samples 2000 --output benchmarks/latest.json`; `benchmarks/run_benchmark.py` → `benchmarks/latest.json` |

### Benchmark scope and reproducibility

```bash
python benchmarks/run_benchmark.py --output benchmarks/latest.json
```

CI reruns the benchmark on every pull request, validates its schema and F1 regression floor, and uploads raw evidence for 30 days. For comparable hosts, median or P95 increases above 15% require investigation and a documented baseline update.

The perfect synthetic classification result is a regression signal for deliberately separated perturbation classes; it is **not** a production accuracy claim. Native C++, service concurrency, network, warehouse, GPU, Firehose/S3 throughput, and real-world labeled drift benchmarks remain future evaluation layers.

### Test and evidence status

| Evidence | Current repository contract | Source |
|---|---|---|
| Drift benchmark raw data | Versioned JSON | `benchmarks/latest.json` |
| Drift benchmark methodology | Versioned report | `benchmarks/benchmark_report.md` |
| Firehose producer validation | Unit-tested configuration + serialized `PutRecord` payloads | `ingestion-service/firehose_test.go` |
| AWS IaC validation | Formatting, provider initialization without backend, Terraform validation | `.github/workflows/aws-telemetry.yml` |
| Local ingestion resilience | Multi-replica NGINX routing and one-replica-loss readiness smoke test | `.github/workflows/ci-cd.yml` |

### Observability metrics

| Metric | Type | Emitted by | Purpose |
|---|---|---|---|
| `ingestion_logs_total{status}` | Counter | `ingestion-service/main.go` | Primary ingestion outcomes |
| `ingestion_handler_seconds` | Histogram | `ingestion-service/main.go` | Ingestion handler latency |
| `ingestion_firehose_records_total{status}` | Counter | `ingestion-service/firehose.go` | Firehose queued, delivered, error, and dropped records |
| `drift_detected_total` | Counter | `drift-engine/server.py` | Drift event count |
| `drift_compute_seconds` | Histogram | `drift-engine/server.py` | Drift calculation latency |
| `llm_guard_summaries_total{method}` | Counter | `llm-guard/app.py` | Ollama vs fallback summary count |
| `llm_guard_summary_seconds` | Histogram | `llm-guard/app.py` | Summary generation latency |

---

## Engineering roadmap

- Add an ephemeral live-AWS integration test that proves Firehose delivery into a disposable S3 prefix without turning normal PR CI into a billable deployment.
- Add `PutRecordBatch` batching and measured queue/backpressure benchmarks before claiming higher producer throughput.
- Add a durable local spool or explicit replay mechanism for mirror records that cannot be lost on process termination.
- Attach the writer policy through an EKS workload identity path and validate least-privilege IAM end to end.
- Add Athena/Glue-compatible telemetry schemas only after a concrete query workload and reproducible evidence exist.
