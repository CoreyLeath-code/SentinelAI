from fastapi import FastAPI
from api.auth import router as auth_router
from api.inference import router as inference_router
from api.rate_limit import limiter
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI(
    title="SentinelAI",
    version="1.0.0",
    description="Production-grade AI inference platform"
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.include_router(auth_router, prefix="/auth")
app.include_router(inference_router, prefix="/infer")

@app.get("/")
def root():
    return {"status": "SentinelAI running"}
