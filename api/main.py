from fastapi import Depends, FastAPI, HTTPException, Header, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from api.inference import run_inference
from pydantic import BaseModel
from typing import List, Optional

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="SentinelAI GPU Inference")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class RequestModel(BaseModel):
    features: List[float]


class PromptRequest(BaseModel):
    prompt: str


def _require_bearer(authorization: Optional[str] = Header(default=None)) -> str:
    """Dependency that validates a Bearer token is present."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    return authorization.removeprefix("Bearer ").strip()


@app.get("/")
def root():
    return {"service": "SentinelAI GPU Inference", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: RequestModel):
    result = run_inference(request.features)
    return {"prediction": result}


_MAX_PROMPT_CHARS = 120


@app.post("/infer")
@limiter.limit("10/minute")
def infer(request: Request, body: PromptRequest, token: str = Depends(_require_bearer)):
    # Stub: return a simple echo response. Replace with LLM call when available.
    return {"response": f"Processed: {body.prompt[:_MAX_PROMPT_CHARS]}"}
