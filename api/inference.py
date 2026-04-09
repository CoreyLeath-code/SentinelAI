_device = None
_model = None


def _get_model():
    """Lazy-load the SentinelModel so torch is only imported when needed."""
    global _device, _model
    if _model is None:
        import torch
        from api.core.model import SentinelModel

        _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        _model = SentinelModel().to(_device)
        _model.eval()
    return _model, _device


def run_inference(features):
    import torch

    model, device = _get_model()
    tensor = torch.tensor(features, dtype=torch.float32).to(device)
    with torch.no_grad():
        output = model(tensor)
    return output.cpu().numpy().tolist()
