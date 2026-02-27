from fastapi import FastAPI
from core.inference import run_inference
from pydantic import BaseModel
from typing import List
import torch

app = FastAPI(title="SentinelAI GPU Inference")

class RequestModel(BaseModel):
    features: List[float]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(request: RequestModel):
    result = run_inference(request.features)
    return {"prediction": result}
