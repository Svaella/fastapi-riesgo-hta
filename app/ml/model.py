
import pandas as pd
from pathlib import Path
from app.core.config import settings
from app.models.patient import PatientInput

# Cargar rutas de modelos desde config
model_path = settings.MODEL_PATH / "rf_model.joblib"
preprocessor_path = settings.MODEL_PATH / "preprocessor.joblib"



def predict_hypertension(patient: PatientInput):
    import joblib
    input_data = pd.DataFrame([patient.dict()])
    # Cargar modelo y preprocesador entrenados
    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)

    print("🔍 INPUT DATA COLUMNS:", input_data.columns.tolist())  # 👈 Añade este print
    print("🔍 INPUT DATA SAMPLE:\n", input_data)

    try:
        processed_data = preprocessor.transform(input_data)
        prob = model.predict_proba(processed_data)[0][1]
    except Exception as e:
        print("❌ ERROR en preprocesamiento:", str(e))
        raise

    if prob >= 0.75:
        riesgo = "Alto"
    elif prob >= 0.5:
        riesgo = "Moderado"
    else:
        riesgo = "Bajo"

    return {
        "riesgo": riesgo,
        "probabilidad": round(prob, 2)
    }