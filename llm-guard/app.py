"""
LLM Guard service — incident summarization using Ollama (optional).

If Ollama is unreachable the service falls back to a rule-based stub so
the rest of the stack keeps running without a local LLM.

Endpoints:
  POST /summarize  — summarize an incident
  GET  /health     — liveness probe
  GET  /metrics    — Prometheus metrics
"""
import logging
import os
from typing import Optional

import psycopg2
import psycopg2.extras
import requests
from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel
from starlette.responses import Response

logger = logging.getLogger(__name__)

app = FastAPI(title="SentinelAI LLM Guard", version="1.0.0")

SUMMARIES_TOTAL   = Counter("llm_guard_summaries_total", "Total summaries generated", ["method"])
SUMMARY_LATENCY   = Histogram("llm_guard_summary_seconds", "Summary latency in seconds")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
LLM_MODEL   = os.getenv("LLM_MODEL", "llama2")
DATABASE_URL = os.getenv("DATABASE_URL", "")
WAREHOUSE_MODE = os.getenv("WAREHOUSE_MODE", "postgres")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_db():
    if WAREHOUSE_MODE != "postgres" or not DATABASE_URL:
        return None
    try:
        return psycopg2.connect(DATABASE_URL, connect_timeout=5)
    except Exception:
        return None


def _ollama_summarize(log_data: str) -> Optional[str]:
    """Call Ollama; return None if unavailable."""
    prompt = (
        "Analyze the following AI inference logs and provide a concise root-cause summary "
        "in 2-3 sentences:\n\n" + log_data
    )
    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": LLM_MODEL, "prompt": prompt, "stream": False},
            timeout=30,
        )
        if resp.status_code == 200:
            return resp.json().get("response", "")
    except requests.RequestException:
        pass
    return None


def _stub_summarize(log_data: str) -> str:
    """Simple rule-based fallback when Ollama is not available."""
    if "psi" in log_data.lower() or "drift" in log_data.lower():
        return "Feature distribution shift detected. Baseline may need refreshing."
    if "latency" in log_data.lower():
        return "Elevated latency observed. Check resource utilization and upstream dependencies."
    return "Anomaly detected in inference pipeline. Manual review recommended."


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class SummarizeRequest(BaseModel):
    incident_id: Optional[int] = None
    log_data: str
    persist: bool = True


class SummarizeResponse(BaseModel):
    incident_id: Optional[int]
    summary: str
    model_used: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok", "service": "llm-guard"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    with SUMMARY_LATENCY.time():
        summary = _ollama_summarize(req.log_data)
        if summary:
            model_used = LLM_MODEL
            SUMMARIES_TOTAL.labels(method="ollama").inc()
        else:
            summary = _stub_summarize(req.log_data)
            model_used = "stub"
            SUMMARIES_TOTAL.labels(method="stub").inc()

    if req.persist and req.incident_id is not None and WAREHOUSE_MODE == "postgres":
        conn = _get_db()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO incident_summaries (incident_id, summary, model_used) VALUES (%s, %s, %s)",
                        (req.incident_id, summary, model_used),
                    )
                conn.commit()
            except Exception:
                logger.exception(
                    "Failed to persist summary for incident_id=%s", req.incident_id
                )
                conn.rollback()
            finally:
                conn.close()

    return SummarizeResponse(incident_id=req.incident_id, summary=summary, model_used=model_used)
