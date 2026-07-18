SentinelAI 
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/33e7a5fb-be0a-495b-a950-7a14b9aedb4b" />

# SentinelAI — Enterprise AI Reliability & Governance Platform

[![CI](https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/ci-cd.yml)
[![Benchmarks](https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/benchmarks.yml/badge.svg)](https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/benchmarks.yml)
[![Security](https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/security.yml/badge.svg)](https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/security.yml)
[![SAST](https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/sast.yml/badge.svg)](https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/sast.yml)
[![Schema Validation](https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/data-validation.yml/badge.svg)](https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/data-validation.yml)
[![Release](https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/release.yml/badge.svg)](https://github.com/CoreyLeath-code/SentinelAI/actions/workflows/release.yml)
[![Coverage](https://img.shields.io/badge/focused%20API%20coverage-24%25-red)](#test-and-evidence-status)
[![Benchmark](https://img.shields.io/badge/reference%20p95-54.7%20%C2%B5s-6f42c1)](benchmarks/benchmark_report.md)
[![Throughput](https://img.shields.io/badge/reference%20throughput-23.0k%20ops%2Fs-2ea44f)](benchmarks/benchmark_report.md)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
---
- Detect model drift
- Monitor inference anomalies
- Track LLM hallucination risk
- Provide real-time observability
- Automate AI governance workflows

It combines statistical ML monitoring with LLM-powered incident intelligence.

## 🏛️ Advanced Platform Architecture & Telemetry Decoupling

To guarantee enterprise-grade performance, SentinelAI enforces strict architectural separation between primary inference loops and the intelligent evaluation layers.
[ Incoming User Query ] ───► [ Async Proxy Gateway ] ───► [ Downstream Application ]
│
(Non-Blocking Telemetry Mirror)
▼
┌──────────────────────────────────────┐
│    SentinelAI Asynchronous Engine    │
├──────────────────────────────────────┤
│  • Parallelized Guardrail Evaluation │
│  • GPT-4 Intelligent SRE Diagnostics │
│  • Token Cost & Allocation Trackers  │
└──────────────────┬───────────────────┘
▼
[ Streamlit Observability Control Plane ]

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
| Ingestion API | http://localhost:8080 |
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

All configuration is via environment variables.  Copy `.env.example` to `.env` and adjust.

| Variable | Default | Description |
|----------|---------|-------------|
| `WAREHOUSE_MODE` | `postgres` | `postgres` (local) or `snowflake` |
| `DATABASE_URL` | Postgres DSN | Full Postgres connection string |
| `POSTGRES_USER` | `sentinel` | Postgres user |
| `POSTGRES_PASSWORD` | `sentinel` | Postgres password |
| `POSTGRES_DB` | `sentinel` | Postgres database |
| `OLLAMA_HOST` | `http://ollama:11434` | Ollama endpoint (optional) |
| `LLM_MODEL` | `llama2` | LLM model name |

**Snowflake (optional):** set `WAREHOUSE_MODE=snowflake` and fill in `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`, `SNOWFLAKE_WAREHOUSE`.

---

## 🏗️ Architecture

```
User → Go Ingestion API (8080) → Postgres (local) / Snowflake (optional)
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
| `ingestion-service` | Go | 8080 | Receives inference logs, writes to warehouse |
| `drift-engine` | C++ + Python | 7070 | PSI/KS drift detection |
| `llm-guard` | Python | 8000 | LLM-powered incident summarization |
| `streamlit-dashboard` | Python | 8501 | Control plane UI |
| `postgres` | — | 5432 | Local warehouse (default) |
| `prometheus` | — | 9090 | Metrics scraping |
| `grafana` | — | 3000 | Dashboards |

---

## 📊 Research Metrics & Benchmarks

The committed baseline is generated by a seeded, dependency-free harness that mirrors the PSI/KS decision rule in the C++ drift engine. These numbers measure the Python reference implementation—not native C++ or end-to-end HTTP latency. See the [full methodology, interpretation, and limitations](benchmarks/benchmark_report.md) and [raw JSON evidence](benchmarks/latest.json).

### Latest reproducible baseline

| Metric | Value | Protocol |
|---|---:|---|
| Timed evaluations | 20,000 | 100 warm-ups, 32 bins, seed `20260718` |
| Mean latency | 41.706 µs | Per-decision reference latency |
| Median latency | 39.700 µs | Per-decision reference latency |
| P95 / P99 latency | 54.700 / 76.200 µs | Linear percentile interpolation |
| Minimum / maximum | 23.700 / 319.200 µs | Observed range |
| Throughput | 23,031.13 operations/s | Single-process CPython reference |
| Peak traced memory | 0.623 MiB | Python `tracemalloc` |
| Precision / recall / F1 | 1.000 / 1.000 / 1.000 | 2,000 balanced synthetic cases |
| Confusion matrix | TP 1000 · TN 1000 · FP 0 · FN 0 | Controlled seeded classes |
| Environment | CPython 3.12.13 · Windows 11 | Recorded 2026-07-18 |

### Benchmark scope and reproducibility

```bash
python benchmarks/run_benchmark.py --output benchmarks/latest.json
```

CI reruns the benchmark on every pull request, validates its schema and F1 regression floor, and uploads raw evidence for 30 days. For comparable hosts, median or P95 increases above 15% require investigation and a documented baseline update.

The perfect synthetic classification result is a regression signal for deliberately separated perturbation classes; it is **not** a production accuracy claim. Native C++, service concurrency, network, warehouse, GPU, and real-world labeled drift benchmarks remain future evaluation layers.

### Test and evidence status

| Evidence | Current state | Source |
|---|---:|---|
| Focused API tests | 4 passed | Existing repository audit |
| Focused API coverage | 24% | Existing repository audit; below 90% target |
| Benchmark raw data | Versioned JSON | `benchmarks/latest.json` |
| Benchmark methodology | Versioned report | `benchmarks/benchmark_report.md` |
| Benchmark CI | Required execution + artifact | `.github/workflows/benchmarks.yml` |
| Drift thresholds | PSI 0.20 · KS 0.10 | `drift-engine/drift_engine.cpp` |

### Observability Metrics

| Metric Name | Type | Emitted By | Purpose |
|---|---|---|---|
| `sentinel_requests_total` | Counter | `monitoring/metrics.py` | API request volume |
| `sentinel_request_latency_seconds` | Histogram | `monitoring/metrics.py` | API request latency |
| `inference_requests_total` | Counter | `monitoring/prometheus.py` | Inference request volume |
| `ingestion_logs_total{status}` | Counter | `ingestion-service/main.go` | Ingestion outcome counts |
| `ingestion_handler_seconds` | Histogram | `ingestion-service/main.go` | Go ingestion handler latency |
| `drift_detected_total` | Counter | `drift-engine/server.py` | Drift event count |
| `drift_compute_seconds` | Histogram | `drift-engine/server.py` | Drift calculation latency |
| `llm_guard_summaries_total{method}` | Counter | `llm-guard/app.py` | Ollama vs fallback summary count |
| `llm_guard_summary_seconds` | Histogram | `llm-guard/app.py` | Summary generation latency |
| `requests_total` | Counter | `backend/app/main.py` | Backend request volume |

### Project & Reproducibility Metrics

| Area | Metric | Current Value | Source |
|---|---:|---:|---|
| Codebase | Tracked files | 98 | `git ls-files` |
| Codebase | Python files | 32 | `*.py` files |
| Codebase | Go files | 1 | `ingestion-service/main.go` |
| Codebase | C++ files | 4 | Drift and ingestion engine sources |
| Codebase | TypeScript files | 7 | `frontend/` |
| Codebase | Source NCLOC | 1,201 | Non-empty, non-comment Python/Go/C++/TS lines |
| Tests | Python test files | 6 | `tests/` |
| Tests | Test declarations | 5 | `def test_*` scan |
| Tests | Focused API validation | 4 passed | `pytest tests/test_*.py` focused API scope |
| Tests | Focused `api` coverage | 24% | Local coverage run |
| CI/CD | GitHub Actions workflows | 7 | `.github/workflows/*.yml` |
| Dependencies | Python runtime dependencies | 11 | `requirements.txt` |
| Delivery | Dockerfiles | 5 | Root/services/dashboard Docker assets |
| Delivery | Kubernetes manifests | 9 | `k8s/*.yaml` |
| Delivery | Helm chart files | 1 | `helm/sentinel/templates/deployment.yaml` |
| Infrastructure | Terraform files | 1 | `terraform/main,TF` |
| Monitoring | Monitoring config files | 5 | `monitoring/` |
| Services | Docker Compose service URLs | 6 | Dashboard, Prometheus, Grafana, ingestion, drift, LLM guard |
| Validation limits | Native Go/C++ compile checks | Not run locally | Go/g++/MSVC unavailable in workspace |

---

## 🧠 Extended Q&A

### Why use C++ for drift detection?
To achieve sub-millisecond statistical scoring at scale.

### Why Go for ingestion?
Go provides efficient concurrency and low-latency HTTP handling.

### Why Postgres locally (not Snowflake)?
Postgres is free, runs in Docker, and supports the same SQL schema.  Switch to `WAREHOUSE_MODE=snowflake` when you're ready to push to production.

### Why MLflow?
Experiment tracking, reproducibility, and version control.

### Why LangChain + Ollama?
LLM-powered root cause summarization and RAG over historical incidents.

### Why Kubernetes?
Horizontal scaling and production-grade orchestration.

### Why Terraform?
Reproducible infrastructure as code.

---

## 🏢 Enterprise Value

SentinelAI demonstrates:

- AI system lifecycle management
- Drift monitoring
- MLOps integration
- Distributed systems engineering
- Cloud-native architecture
- LLM augmentation
- Observability & metrics-driven design

---

## 🔧 Recent Code Improvements

The following fixes were applied to improve reliability, correctness, and security:

| File | Issue | Fix |
|------|-------|-----|
| `api/core/model.py` *(new)* | `core.model` module was missing, crashing on import | Created `SentinelModel` (two-layer MLP) as a proper PyTorch module |
| `api/__init__.py` *(new)* | Package not importable as `api.*` | Added package init file |
| `api/inference.py` | `from core.model import …` caused `ModuleNotFoundError` | Updated to `from api.core.model import SentinelModel` |
| `api/main.py` | `from core.inference import …` caused `ModuleNotFoundError`; missing `GET /` route | Updated import to `from api.inference import run_inference`; added root route |
| `api/auth.py` | Hardcoded `admin/admin` credentials | Reads `API_USERNAME` / `API_PASSWORD` from environment; rejects auth when `API_PASSWORD` is unset |
| `api/routes/inference.py` | Model loaded at import time (blocks startup, crashes without GPU/HuggingFace access); `device_map="auto"` forced CUDA | Lazy-loads model on first request; model name configurable via `LLM_MODEL_NAME` env var; CPU fallback added |
| `backend/app/main.py` | `.cuda()` called unconditionally (crashes on CPU-only hosts); MLflow `start_run()` ran at module level (import fails if MLflow unreachable) | Added `cpu/cuda` device selection; wrapped MLflow block in `try/except` |
| `llm-guard/app.py` | `except Exception: pass` silently swallowed DB errors | Replaced with `logger.exception(…)` + `conn.rollback()` |
| `tests/conftest.py` | `from app.main import app` — wrong package path, caused all tests to fail | Fixed to `from api.main import app` |
| `requirements.txt` | Missing `httpx` (required by FastAPI `TestClient`) and `pydantic` | Added both packages |

### Running tests locally

```bash
pip install -r requirements.txt
pytest tests/ -v
```

### Environment variables added

| Variable | Default | Description |
|----------|---------|-------------|
| `API_USERNAME` | `admin` | Login username for the API auth endpoint |
| `API_PASSWORD` | *(unset — auth disabled until set)* | Login password; must be set to enable auth |
| `LLM_MODEL_NAME` | `meta-llama/Meta-Llama-3-8B` | HuggingFace model used by the inference route |

---



- Add automated retraining pipeline
- Add Shadow Model Deployment
- Add Cost Optimization Engine
- Add Hallucination Classifier Model




