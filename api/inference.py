from fastapi import APIRouter
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

router = APIRouter()

MODEL_NAME = "meta-llama/Meta-Llama-3-8B"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

@router.post("/")
def infer(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=100)
    return {"response": tokenizer.decode(output[0], skip_special_tokens=True)}
