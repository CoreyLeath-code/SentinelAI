# SentinelAI — System Design

## 1. Overview

SentinelAI is an enterprise AI reliability and monitoring platform designed to detect:
- Model drift
- Data drift
- LLM hallucination risk
- Inference anomalies
- Latency spikes
- Cost overruns

It combines classical ML monitoring with LLM-based incident summarization.

---

## 2. Architecture

### Ingestion Layer (Go)
- Receives inference logs
- Tracks latency, tokens, errors
- Sends structured logs to Snowflake

### Storage Layer (Snowflake)
- Feature storage
- Drift baseline tables
- Historical inference logs

### Drift Engine (C++)
- KS test
- Population Stability Index (PSI)
- Real-time statistical scoring

### ML Training Layer (AWS SageMaker)
- Model training
- Versioning
- MLflow experiment tracking

### LLM Guard (LangChain + Ollama)
- Incident summarization
- RAG-based historical lookup
- Hallucination scoring

### UI Layer (Streamlit)
- Drift visualization
- Latency dashboards
- Incident summaries
- Infrastructure metrics

---

## 3. Deployment

- Docker containers
- Kubernetes (EKS)
- Helm charts
- Terraform IaC
- GitHub Actions CI/CD

---

## 4. Scaling Strategy

- Horizontal pod autoscaling
- Model shadow deployment
- Canary releases
- Drift-triggered retraining

---

## 5. Observability

- MLflow experiment tracking
- Drift scoring logs
- Prometheus-ready metrics
- Cost-per-1k inference tracking
