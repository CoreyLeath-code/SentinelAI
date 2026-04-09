import logging
import os
import sys

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/infer", tags=["Inference"])

logger = logging.getLogger(__name__)

_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "meta-llama/Meta-Llama-3-8B")

_tokenizer = None
_model = None
_device = None


def _load_model():
    """Lazy-load the model and tokenizer on first request."""
    global _tokenizer, _model, _device
    if _model is not None:
        return
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    _device = "cuda" if torch.cuda.is_available() else "cpu"
    try:
        logger.info("Loading model %s onto %s …", _MODEL_NAME, _device)
        _tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
        _model = AutoModelForCausalLM.from_pretrained(
            _MODEL_NAME,
            torch_dtype=torch.float16 if _device == "cuda" else torch.float32,
            device_map="auto" if _device == "cuda" else None,
        )
        if _device != "cuda":
            _model = _model.to(_device)
        logger.info("Model loaded successfully.")
    except Exception as exc:
        logger.error("Failed to load model %s: %s", _MODEL_NAME, exc)
        raise RuntimeError(f"Model {_MODEL_NAME!r} could not be loaded: {exc}") from exc


class Prompt(BaseModel):
    text: str


@router.post("/")
def run_inference(prompt: Prompt):
    try:
        _load_model()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    torch = sys.modules["torch"]
    inputs = _tokenizer(prompt.text, return_tensors="pt").to(_device)
    with torch.no_grad():
        output = _model.generate(**inputs, max_new_tokens=128)
    return {"response": _tokenizer.decode(output[0], skip_special_tokens=True)}

