"""
Drift-engine HTTP service.

Wraps the compiled C++ drift_engine binary with a FastAPI interface.
Endpoints:
  POST /drift   — compute PSI + KS for a pair of histograms
  GET  /health  — liveness probe
  GET  /metrics — Prometheus metrics
"""
import json
import os
import subprocess
from typing import List

from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel
from starlette.responses import Response

app = FastAPI(title="SentinelAI Drift Engine", version="1.0.0")

DRIFT_DETECTED = Counter("drift_detected_total", "Number of drift events detected")
DRIFT_LATENCY  = Histogram("drift_compute_seconds", "Drift computation latency")


class DriftRequest(BaseModel):
    model_id: str = "default"
    feature_name: str = "default"
    expected: List[float]
    actual: List[float]


class DriftResponse(BaseModel):
    model_id: str
    feature_name: str
    psi: float
    ks_stat: float
    drift_detected: bool


@app.get("/health")
def health():
    return {"status": "ok", "service": "drift-engine"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/drift", response_model=DriftResponse)
def compute_drift(req: DriftRequest):
    payload = json.dumps({"expected": req.expected, "actual": req.actual})
    binary = os.path.join(os.path.dirname(__file__), "drift_engine")

    with DRIFT_LATENCY.time():
        try:
            proc = subprocess.run(
                [binary],
                input=payload.encode(),
                capture_output=True,
                timeout=10,
            )
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="drift_engine binary not found")
        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=504, detail="drift_engine timed out")

    if proc.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail=f"drift_engine error: {proc.stderr.decode()}"
        )

    try:
        result = json.loads(proc.stdout.decode())
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"invalid output: {exc}")

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    if result.get("drift_detected"):
        DRIFT_DETECTED.inc()

    return DriftResponse(
        model_id=req.model_id,
        feature_name=req.feature_name,
        psi=result["psi"],
        ks_stat=result["ks_stat"],
        drift_detected=result["drift_detected"],
    )
