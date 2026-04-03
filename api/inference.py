import torch
from api.core.model import SentinelModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SentinelModel().to(device)
model.eval()

def run_inference(features):
    tensor = torch.tensor(features, dtype=torch.float32).to(device)
    with torch.no_grad():
        output = model(tensor)
    return output.cpu().numpy().tolist()
