from fastapi import APIRouter, HTTPException
from app.models.patient import PatientInput, PredictionResult
from app.ml.model import predict_hypertension


router = APIRouter()

@router.post("/predict", response_model=PredictionResult)
async def predict(patient: PatientInput):
    """
    Predice el riesgo de hipertensión arterial basado en los datos del paciente.
    
    Utiliza un modelo de Random Forest entrenado con datos demográficos y de estilo de vida.
    """
    try:
        result = predict_hypertension(patient)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la predicción: {str(e)}")

@router.get("/health")
async def health_check():
    """Endpoint para verificar que la API está funcionando correctamente"""
    return {"status": "ok"}