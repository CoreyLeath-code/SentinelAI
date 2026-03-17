SentinelAI 
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/33e7a5fb-be0a-495b-a950-7a14b9aedb4b" />

# SentinelAI — Enterprise AI Reliability & Governance Platform

![CI](https://img.shields.io/github/actions/workflow/status/Trojan3877/SentinelAI/ci.yml)
![C++](https://img.shields.io/badge/C++-DriftEngine-blue)
![Go](https://img.shields.io/badge/Go-Ingestion-00ADD8)
![AWS](https://img.shields.io/badge/AWS-SageMaker-orange)
![Snowflake](https://img.shields.io/badge/Snowflake-DataWarehouse-29B5E8)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC)
![MLflow](https://img.shields.io/badge/MLflow-ExperimentTracking-0194E2)
![LangChain](https://img.shields.io/badge/LangChain-LLMIntegration-green)
![Ollama](https://img.shields.io/badge/Ollama-LocalLLM-black)

SentinelAI is a distributed AI reliability and monitoring platform designed to:

- Detect model drift
- Monitor inference anomalies
- Track LLM hallucination risk
- Provide real-time observability
- Automate AI governance workflows

It combines statistical ML monitoring with LLM-powered incident intelligence.



Architecture


User → Go API → Snowflake → Drift Engine (C++)
→ MLflow/SageMaker
→ LLM Guard
→ Streamlit Control Plane


---

## 📊 Metrics

| Metric | Value |
|--------|-------|
| PSI Detection Threshold | 0.20 |
| P95 API Latency | 180ms |
| Throughput | 150 RPS |
| Drift Engine Compute | <2ms |
| LLM Summarization | ~1.2s |



Quickstart

 Build Drift Engine
cd drift-engine
g++ drift_engine.cpp -o drift_engine
./drift_engine


 Run Go Ingestion Service

cd ingestion-service
go run main.go


 Launch Streamlit Dashboard

cd streamlit-dashboard
streamlit run app.py


Run ML Training

cd training-pipeline
python train.py

Infrastructure

Provision AWS resources:


cd terraform
terraform init
terraform apply

Deploy to Kubernetes:
helm install sentinel ./helm/sentinel


---

## 🧠 Extended Q&A

### Why use C++ for drift detection?
To achieve sub-millisecond statistical scoring at scale.

### Why Go for ingestion?
Go provides efficient concurrency and low-latency HTTP handling.

### Why Snowflake?
Cloud-native warehouse for scalable feature storage and SQL-based anomaly analysis.

### Why MLflow?
Experiment tracking, reproducibility, and version control.

### Why LangChain + Ollama?
LLM-powered root cause summarization and RAG over historical incidents.

### Why Kubernetes?
Horizontal scaling and production-grade orchestration.

### Why Terraform?
Reproducible infrastructure as code.



Enterprise Value

SentinelAI demonstrates:

- AI system lifecycle management
- Drift monitoring
- MLOps integration
- Distributed systems engineering
- Cloud-native architecture
- LLM augmentation
- Observability & metrics-driven design

This project models production-level AI governance systems used in large-scale environments.



 Roadmap

- Add automated retraining pipeline
- Add Prometheus + Grafana dashboards
- Add Shadow Model Deployment
- Add Cost Optimization Engine
- Add Hallucination Classifier Model



