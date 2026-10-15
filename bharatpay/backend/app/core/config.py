import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "BharatPay Neobank"
    API_V2_STR: str = "/api/v2"
    SECRET_KEY: str = os.getenv("JWT_SECRET", "synthetic_demo_jwt_secret_cc6_ic07_bharatpay")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./bharatpay.db")
    LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH", "./logs/bharatpay_requests.jsonl")
    
    # Environment flag
    ENV_NAME: str = "synthetic-demo"
    DATA_WATERMARK: str = "SYNTHETIC TEST DATA — CC6-IC07"

    class Config:
        case_sensitive = True

settings = Settings()
