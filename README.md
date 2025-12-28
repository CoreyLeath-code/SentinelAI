SentinelAI 
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/33e7a5fb-be0a-495b-a950-7a14b9aedb4b" />

# 🛡 SentinelAI — Production-Grade AI Inference Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-green)
![CUDA](https://img.shields.io/badge/NVIDIA-CUDA-success)
![Kubernetes](https://img.shields.io/badge/Kubernetes-GPU-blue)
![CI/CD](https://img.shields.io/badge/GitHub%20Actions-CI/CD-brightgreen)
![MLFlow](https://img.shields.io/badge/MLflow-Tracking-blue)
![L7](https://img.shields.io/badge/Engineering%20Level-L7-black)

SentinelAI is a **full-stack, GPU-accelerated AI inference platform** designed for **real-world production deployment**.  
Built with **FastAPI, CUDA, Llama 3, Kubernetes, CI/CD, MLFlow, Prometheus, and Streamlit**.

---

## 🚀 Features

- 🔥 Llama 3 inference (CUDA-accelerated)
- ⚡ FastAPI REST API
- 📊 Streamlit live dashboard
- 📦 Docker + Render deployment
- ☸️ Kubernetes GPU orchestration
- 📈 Prometheus monitoring
- 🤖 N8N automation workflows
- 🔐 Rate-limiting & auth ready
- 🧪 Test suite + CI/CD

---

## 🧠 System Architecture

![SentinelAI Architecture](SentinelAI_Architecture.png)

---

## ⚙️ Quick Start

```bash
git clone https://github.com/Trojan3877/SentinelAI
cd SentinelAI
pip install -r requirements.txt
uvicorn api.main:app --reload





 
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/4cbc93b4-a7ba-4615-9ddb-82f06745151a" />


🧰 Tech Stack
Frontend

Next.js (TypeScript)

Tailwind CSS

Streamlit (Live Metrics Dashboard)

Backend

FastAPI

Llama 3 (CUDA)

Auth + Rate Limiting

MLflow Experiment Tracking

Infrastructure

Docker

Kubernetes (GPU scheduling)

Prometheus

Render Deployment

GitHub Actions CI/CD

⚡ Quick Start (Local)
docker compose up --build


API → http://localhost:8000

UI → http://localhost:3000

☸️ Kubernetes Deployment
kubectl apply -f k8s/


Supports NVIDIA GPU nodes, metrics scraping, and horizontal scaling.

🧪 Testing
pytest tests/


Includes:

Health checks

Auth validation

Rate limiting

LLM inference validation

📊 Observability

/metrics → Prometheus

MLflow UI → experiment tracking

Streamlit → live dashboard

🎯 Why SentinelAI

✔ Production-ready
✔ GPU-accelerated
✔ Full-stack TypeScript + Python
✔ MLOps + Platform Engineering
✔ Recruiter-credible system design

Design Questions & Reflections

Q: What problem does this project aim to solve?
A: SentinelAI is designed to explore how a real-time monitoring and alerting system could automatically detect and respond to important changes in live streams of data. The goal wasn’t just to build alerts, but to investigate how pattern detection, rule-based triggers, and scalable event processing work together in a monitoring pipeline that could be extended to different domains.

Q: Why did I choose this approach instead of alternatives?
A: I chose a modular architecture that separates ingestion, detection, and notification logic to make it easier to experiment with different detection strategies and scale individual components independently. This was more complex than a monolithic script, but allowed clearer reasoning about how each part contributes to overall behavior.

Q: What were the main trade-offs I made?
A: The trade-off was flexibility versus immediate simplicity — I could have built a quick script that triggered hard-coded alerts, but that wouldn’t scale or adapt to varied signal types. By building modular components and using an event-driven mindset, I gained clarity and extensibility at the cost of added upfront complexity.

Q: What didn’t work as expected?
A: One challenge was balancing false positives versus detection sensitivity. Initially, the system generated too many alerts — most of them not meaningful — which made it harder to trust outputs. That forced me to think about thresholds and event aggregation rather than just adding more detection rules.

Q: What did I learn from building this project?
A: I learned how critical evaluation and tuning are when moving from simple logic to production-style detection systems. Building observability into the system early helped me understand failure patterns and iteratively refine detection criteria rather than guessing at configurations.

Q: If I had more time or resources, what would I improve next?
A: I would add more advanced anomaly detection modules using basic statistical techniques or lightweight ML models so the system could adapt its sensitivity over time. I’d also build clearer logging and dashboard integration so a user could visually explore why alerts were generated.




👤 Author

Corey Leath
Senior Software Engineering Student
AI / ML / Platform Engineering
https://github.com/Trojan3877
