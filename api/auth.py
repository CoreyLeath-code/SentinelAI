import os

from fastapi import APIRouter, HTTPException

router = APIRouter()

_API_USERNAME = os.getenv("API_USERNAME", "admin")
_API_PASSWORD = os.getenv("API_PASSWORD", "")


@router.post("/login")
def login(username: str, password: str):
    if not _API_PASSWORD:
        raise HTTPException(
            status_code=500,
            detail="Server authentication is not configured (API_PASSWORD unset)",
        )
    if username == _API_USERNAME and password == _API_PASSWORD:
        return {"token": "sentinel-jwt-placeholder"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
