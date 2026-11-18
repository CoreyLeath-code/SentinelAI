"""SentinelModel inference must use a verified trained checkpoint.

Never return predictions from a freshly initialized random-weight model.
"""

import hashlib
import hmac
import os
from pathlib import Path

_device = None
_model = None


def _verified_checkpoint() -> Path:
    """Require an operator-supplied immutable artifact fingerprint before loading."""
    path_value = os.environ.get("SENTINEL_MODEL_CHECKPOINT")
    expected_sha = os.environ.get("SENTINEL_MODEL_SHA256")
    if not path_value or not expected_sha:
        raise RuntimeError("A verified model checkpoint is not configured")
    if len(expected_sha) != 64 or any(c not in "0123456789abcdefABCDEF" for c in expected_sha):
        raise RuntimeError("SENTINEL_MODEL_SHA256 must be a 64-character hex digest")
    path = Path(path_value).resolve()
    if not path.is_file():
        raise RuntimeError("Configured model checkpoint is unavailable")
    digest = hashlib.sha256()
    with path.open("rb") as artifact:
        for chunk in iter(lambda: artifact.read(64 * 1024), b""):
            digest.update(chunk)
    if not hmac.compare_digest(digest.hexdigest(), expected_sha.lower()):
        raise RuntimeError("Model checkpoint fingerprint verification failed")
    return path


def _get_model():
    """Load a known checkpoint; fail closed rather than use untrained weights."""
    global _device, _model
    if _model is None:
        checkpoint = _verified_checkpoint()
        import torch
        from api.core.model import SentinelModel

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Only load tensor weights, not arbitrary Python objects in pickle data.
        weights = torch.load(checkpoint, map_location=device, weights_only=True)
        if not isinstance(weights, dict):
            raise RuntimeError("Model checkpoint must contain a state dictionary")
        model = SentinelModel().to(device)
        model.load_state_dict(weights, strict=True)
        model.eval()
        _device = device
        _model = model
    return _model, _device


def run_inference(features):
    import torch

    model, device = _get_model()
    tensor = torch.tensor(features, dtype=torch.float32).to(device)
    with torch.no_grad():
        output = model(tensor)
    return output.cpu().numpy().tolist()
