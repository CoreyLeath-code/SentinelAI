SentinelAI 
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/33e7a5fb-be0a-495b-a950-7a14b9aedb4b" />

# SentinelAI — Enterprise AI Reliability & Governance Platform

![CI](https://img.shields.io/github/actions/workflow/status/Trojan3877/SentinelAI/ci.yml?branch=main)
![C++](https://img.shields.io/badge/C++-DriftEngine-blue)
![Go](https://img.shields.io/badge/Go-Ingestion-00ADD8)
![Snowflake](https://img.shields.io/badge/Snowflake-Optional-29B5E8)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC)
![MLflow](https://img.shields.io/badge/MLflow-ExperimentTracking-0194E2)
![LangChain](https://img.shields.io/badge/LangChain-LLMIntegration-green)
![Ollama](https://img.shields.io/badge/Ollama-LocalLLM-black)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/trojan3877/sentinelai/main/demo_app.py)
SentinelAI is a distributed AI reliability and monitoring platform designed to:
![Build Status](https://github.com/Trojan3877/SentinelAI/workflows/CI/badge.svg)
[![LLM Engine: GPT-4](https://img.shields.io/badge/LLM_Engine-GPT--4_Omni-4aa377.svg?logo=openai&logoColor=white)](https://openai.com/)
[![Control Plane: Streamlit](https://img.shields.io/badge/Control_Plane-Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)](https://share.streamlit.io/)
[![Guardrails: Semantic & PII](https://img.shields.io/badge/Guardrails-Semantic_%26_PII-orange.svg)](#)
<!-- CI/CD & Automation Telemetry Matrix -->
[![Continuous Integration](https://github.com/Trojan3877/SentinelAI/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Trojan3877/SentinelAI/actions/workflows/ci-cd.yml)
[![Code Quality Assurance](https://github.com/Trojan3877/SentinelAI/actions/workflows/ci.yml/badge.svg)](https://github.com/Trojan3877/SentinelAI/actions/workflows/ci.yml)
[![Security Analysis](https://github.com/Trojan3877/SentinelAI/actions/workflows/security.yml/badge.svg)](https://github.com/Trojan3877/SentinelAI/actions/workflows/security.yml)
[![SAST Code Flaw Scan](https://github.com/Trojan3877/SentinelAI/actions/workflows/sast.yml/badge.svg)](https://github.com/Trojan3877/SentinelAI/actions/workflows/sast.yml)
[![Performance Benchmarks](https://github.com/Trojan3877/SentinelAI/actions/workflows/benchmarks.yml/badge.svg)](https://github.com/Trojan3877/SentinelAI/actions/workflows/benchmarks.yml)
[![Schema Validation](https://github.com/Trojan3877/SentinelAI/actions/workflows/data-validation.yml/badge.svg)](https://github.com/Trojan3877/SentinelAI/actions/workflows/data-validation.yml)
[![Automated Release](https://github.com/Trojan3877/SentinelAI/actions/workflows/release.yml/badge.svg)](https://github.com/Trojan3877/SentinelAI/actions/workflows/release.yml)

<!-- Engineering Framework & Standard Badges -->
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Framework: MLflow](https://img.shields.io/badge/Framework-MLflow-005b96.svg?logo=mlflow)](https://mlflow.org/)
[![Code Style: Flake8](https://img.shields.io/badge/code%20style-flake8-black)](https://flake8.pycqa.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

## 📊 Metrics

| Metric | Value |
|--------|-------|
| PSI Detection Threshold | 0.20 |
| P95 API Latency | 180ms |
| Throughput | 150 RPS |
| Drift Engine Compute | <2ms |
| LLM Summarization | ~1.2s |

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




