import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "CRM Management System - TTCS"
    PROJECT_DESCRIPTION: str = "Hệ thống Quản lý Khách hàng (CRM) - Backend FastAPI với cơ chế xử lý lỗi tập trung SCRUM-38"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # JWT Security Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "crm-ttcs-super-secret-jwt-key-for-scrum-38-security")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
