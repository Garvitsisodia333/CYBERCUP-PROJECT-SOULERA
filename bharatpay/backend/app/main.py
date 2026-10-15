import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
import app.models  # Ensures all models are registered

# Create SQLite tables if they do not exist
Base.metadata.create_all(bind=engine)

# Ensure logs directory exists
os.makedirs(os.path.dirname(settings.LOG_FILE_PATH), exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Fictional UPI Neobank API - Target testbed for CC6-IC07 API Discovery & Abuse Prevention",
    version="2.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.middleware.structured_logger import StructuredLoggingMiddleware
app.add_middleware(StructuredLoggingMiddleware)

from app.api.v2.auth import router as auth_router
app.include_router(auth_router, prefix="/api/v2")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "bharatpay-backend",
        "version": "2.0.0",
        "watermark": settings.DATA_WATERMARK
    }

@app.get("/")
def root():
    return {
        "message": "Welcome to BharatPay API",
        "environment": settings.ENV_NAME,
        "watermark": settings.DATA_WATERMARK
    }
