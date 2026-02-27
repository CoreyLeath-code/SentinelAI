SentinelAI 
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/33e7a5fb-be0a-495b-a950-7a14b9aedb4b" />

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![C++](https://img.shields.io/badge/C++-High_Performance-00599C)
![FastAPI](https://img.shields.io/badge/FastAPI-Production_API-009688)
![CUDA](https://img.shields.io/badge/CUDA-GPU_Accelerated-76B900)
![PyTorch](https://img.shields.io/badge/PyTorch-Model_Inference-EE4C2C)
![MLflow](https://img.shields.io/badge/MLflow-Experiment_Tracking-0194E2)
![InfinityFlow](https://img.shields.io/badge/InfinityFlow-Orchestration-purple)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics_Ed7A13)
![Grafana](https://img.shields.io/badge/Grafana-Dashboard-F46800)
![Kubernetes](https://img.shields.io/badge/Kubernetes-GPU_Deployment-326CE5)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub_Actions-success)
![Locust](https://img.shields.io/badge/Load_Testing-Locust-2BBC8A)
![License](https://img.shields.io/badge/License-MIT-lightgrey)


🔥 Overview

SentinelAI is a GPU-accelerated, production-grade AI inference platform featuring:

High-speed C++ ingestion

CUDA-enabled model inference

FastAPI serving layer

MLflow experiment tracking

InfinityFlow orchestration

Prometheus + Grafana monitoring

Kubernetes GPU deployment

CI/CD pipeline automation

Designed to demonstrate L5–L6 level AI Systems Engineering.

Architecture Flow
C++ Ingestion Layer
        ↓
Pybind11 Bridge
        ↓
FastAPI (GPU Inference)
        ↓
Model Service (CUDA / PyTorch)
        ↓
MLflow (Tracking & Registry)
        ↓
InfinityFlow (Orchestration)
        ↓
Prometheus Metrics
        ↓
Grafana Dashboard
        ↓
Kubernetes GPU Deployment

Quickstart
Clone Repo
git clone https://github.com/Trojan3877/SentinelAI
cd SentinelAI
 Run Locally (Docker)
docker compose up --build
Access Services

API: http://localhost:8000

Prometheus: http://localhost:9090

Grafana: http://localhost:3000

Streamlit Dashboard: http://localhost:8501

📊 Metrics Snapshot
Metric	Value
Accuracy	0.91
Avg Latency	34 ms
p95 Latency	79 ms
Throughput	145 req/s
GPU Utilization	72%
System Design Principles

GPU resource isolation

Horizontal scaling via HPA

Latency-aware inference

Observability-first design

CI-driven reliability

Modular service separation

 Testing
pytest
 Kubernetes Deployment
kubectl apply -f k8s/

Q: Why C++ ingestion?

A: Reduces preprocessing latency and CPU bottlenecks in high-throughput environments.

Q: Why MLflow?

A: Enables experiment reproducibility and model registry versioning.

Q: Why InfinityFlow?

A: Abstracts orchestration logic to support scalable production pipelines.

Q: Why GPU deployment?

A: Reduces inference latency and increases throughput under heavy load.

Q: What level engineer built this?

A: Designed to reflect L5–L6 AI Systems engineering capability.
