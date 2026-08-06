# Changelog

## 2026-08-05

### Recent Code Improvements

| File | Issue | Fix |
|------|-------|-----|
| `api/core/model.py` *(new)* | `core.model` module was missing, crashing on import | Created `SentinelModel` (two-layer MLP) as a proper PyTorch module |
| `api/__init__.py` *(new)* | Package not importable as `api.*` | Added package init file |
| `api/inference.py` | `from core.model import …` caused `ModuleNotFoundError` | Updated to `from api.core.model import SentinelModel` |
| `api/main.py` | `from core.inference import …` caused `ModuleNotFoundError`; missing `GET /` route | Updated import to `from api.inference import run_inference`; added root route |
| `api/auth.py` | Hardcoded `admin/admin` credentials | Reads `API_USERNAME` / `API_PASSWORD` from environment; rejects auth when `API_PASSWORD` is unset |
| `api/routes/inference.py` | Model loaded at import time (blocks startup, crashes without GPU/HuggingFace access); `device_map="auto"` forced CUDA | Lazy-loads model on first request; model name configurable via `LLM_MODEL_NAME` env var; CPU fallback added |
| `backend/app/main.py` | `.cuda()` called unconditionally (crashes on CPU-only hosts); MLflow `start_run()` ran at module level (import fails if MLflow unreachable) | Added `cpu/cuda` device selection; wrapped MLflow block in `try/except` |
| `llm-guard/app.py` | `except Exception: pass` silently swallowed DB errors | Replaced with `logger.exception(…)` + `conn.rollback()` |
| `tests/conftest.py` | `from app.main import app` — wrong package path, caused all tests to fail | Fixed to `from api.main import app` |
| `requirements.txt` | Missing `httpx` (required by FastAPI `TestClient`) and `pydantic` | Added both packages |
