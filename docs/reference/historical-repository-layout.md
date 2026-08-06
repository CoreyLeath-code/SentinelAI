# Historical repository layout reference

This manually maintained snapshot was moved from the repository root during the 2026-08-05 root-directory audit. It is retained for historical context only and is **not** a generated current inventory; use the repository tree and service documentation for current paths.

## Original snapshot

```text
SentinelAI/
│
├── ingestion-service/           # Go - Log ingestion + API gateway
│
├── drift-engine/                # C++ - High-performance statistical drift detection
│
├── training-pipeline/           # Python - SageMaker training + MLflow tracking
│
├── llm-guard/                   # LangChain + Ollama - RAG + incident summarization
│
├── streamlit-dashboard/         # Streamlit - AI Observability UI
│   ├── app.py
│   ├── pages/
│   │   ├── 1_Model_Drift.py
│   │   ├── 2_LLM_Monitoring.py
│   │   ├── 3_Incident_Summary.py
│   │   ├── 4_System_Metrics.py
│   │
│   ├── components/
│   │   ├── charts.py
│   │   ├── drift_visualizer.py
│   │   ├── latency_graphs.py
│   │
│   └── requirements.txt
│
├── docker/                      # Dockerfiles for all services
│
├── helm/                        # Kubernetes Helm charts
│
├── terraform/                   # Infrastructure as Code
│
├── ci-cd/                       # GitHub Actions workflows
│
├── metrics.md                   # Evaluation metrics + performance benchmarks
│
├── system_design.md             # Architecture deep dive
│
├── architecture.png             # Visual diagram
│
└── README.md                    # Recruiter-facing explanation
SentinelAI/
│
├── app/
│   └── streamlit_app.py
├── src/
├── requirements.txt
├── README.md
```
