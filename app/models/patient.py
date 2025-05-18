from pydantic import BaseModel, Field, field_validator
from enum import Enum

class PatientInput(BaseModel):
    Gender: str
    Age: float = Field(..., ge=0, le=100)
    BMI: float = Field(..., ge=0, le=100)
    Physical_Activity_Level: str
    Sleep_Duration: float = Field(..., ge=0, le=24)
    Smoking_Status: str
    Family_History: str
    Stress_Level: int = Field(..., ge=1, le=9)

class PredictionResult(BaseModel):
    riesgo: str
    probabilidad: float