# backend/app/main.py
import logging

import mlflow
import mlflow.pytorch
import torch
from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest

logger = logging.getLogger(__name__)

app = FastAPI()

_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_MODEL_LABEL = "cuda-inference" if _device.type == "cuda" else "cpu-inference"

# Log MLflow experiment metadata at startup — failure is non-fatal.
try:
    mlflow.set_tracking_uri("http://mlflow:5000")
    with mlflow.start_run():
        mlflow.log_param("model", _MODEL_LABEL)
        mlflow.log_metric("latency_ms", 12.4)
except Exception:
    logger.warning("MLflow tracking unavailable — continuing without experiment logging.")

REQUESTS = Counter("requests_total", "Total requests")


@app.middleware("http")
async def metrics_middleware(request, call_next):
    REQUESTS.inc()
    return await call_next(request)


@app.get("/health")
def health():
    return {"status": "ok", "cuda": torch.cuda.is_available()}


@app.post("/predict")
def predict(data: list[float]):
    tensor = torch.tensor(data).to(_device)
    result = tensor.mean().item()
    return {"prediction": result}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
