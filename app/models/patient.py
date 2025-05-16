from pydantic import BaseModel, Field, field_validator
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class SmokingStatus(str, Enum):
    NEVER = "never"
    FORMER = "former"
    CURRENT = "current"

class PhysicalActivityLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"

class MedicalHistory(str, Enum):
    YES = "yes"
    NO = "no"

class PatientInput(BaseModel):
    sexo: Gender
    edad: int = Field(..., ge=0, le=100)
    peso: float = Field(..., gt=0, le=300)  # en kg
    altura: float = Field(..., gt=0, le=300)  # en centímetros
    fumador: SmokingStatus
    actividadFisica: PhysicalActivityLevel
    sueno: float = Field(..., ge=0, le=24)  # horas de sueño
    antecedentesHipertension: MedicalHistory
    
    @field_validator('sueno')
    def redondear_sueno(cls, v):
        return round(v)
    
    class Config:
        schema_extra = {
            "example": {
                "sexo": "male", # hombre
                "edad": 45,
                "peso": 80.5,   # en kg
                "altura": 175,  # en centímetros
                "fumador": "never", # nunca
                "actividadFisica": "moderate",  #moderado
                "sueno": 7,
                "antecedentesHipertension": "no"
            }
        }

class PredictionResult(BaseModel):
    riesgo_hipertension: bool
    probabilidad: float
    #imc: float
    #categoria_imc: str
    #recomendaciones: list[str]