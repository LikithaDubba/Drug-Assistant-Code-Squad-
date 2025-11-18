# backend/app/main.py
from fastapi import FastAPI
from app.api_routes import router as api_router

app = FastAPI(title="Drug Assistant API", version="0.1")

app.include_router(api_router, prefix="/api")
