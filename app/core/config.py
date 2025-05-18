from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # ✅ /app
MODEL_DIR = BASE_DIR / "model"  # ✅ /app/model

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sistema de Valoración de Riesgo de Hipertensión Arterial"
    MODEL_PATH: Path = MODEL_DIR
    
    class Config:
        case_sensitive = True

settings = Settings()