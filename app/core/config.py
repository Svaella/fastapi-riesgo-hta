from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sistema de Valoración de Riesgo de Hipertensión Arterial"
    MODEL_PATH: Path = BASE_DIR / "model" / "random_forest_model.joblib"
    
    class Config:
        case_sensitive = True

settings = Settings()