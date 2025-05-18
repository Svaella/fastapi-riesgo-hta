import pandas as pd
from pathlib import Path
import requests
from app.core.config import settings
from app.models.patient import PatientInput
import joblib


def descargar_desde_drive(file_id, output_path):
    output_path = Path(output_path)
    if not output_path.exists():
        print(f"📥 Descargando modelo desde Google Drive a {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(url)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Descargado: {output_path}")


def predict_hypertension(patient: PatientInput):
    # 📌 Definir rutas
    model_path = settings.MODEL_PATH / "rf_model.joblib"
    preprocessor_path = settings.MODEL_PATH / "preprocessor.joblib"

    # 📥 Descargar si no existe localmente
    descargar_desde_drive("I1yhLc3gmiqawy-OmRxF774K9rZoPj72fg", model_path)
    descargar_desde_drive("11-k2AdEJ5T_qBFfDK8yq7rz-x3iv25gO", preprocessor_path)

    # 📊 Preparar datos
    input_data = pd.DataFrame([patient.dict()])
    print("🔍 INPUT DATA COLUMNS:", input_data.columns.tolist())
    print("🔍 INPUT DATA SAMPLE:\n", input_data)

    # ⚙️ Cargar modelo y preprocesador
    try:
        model = joblib.load(model_path)
        preprocessor = joblib.load(preprocessor_path)
        processed_data = preprocessor.transform(input_data)
        prob = model.predict_proba(processed_data)[0][1]
    except Exception as e:
        print("❌ ERROR en preprocesamiento:", str(e))
        raise

    # 📈 Clasificación de riesgo
    if prob >= 0.75:
        riesgo = "Alto"
    elif prob >= 0.5:
        riesgo = "Moderado"
    else:
        riesgo = "Bajo"

    return {
        "riesgo": riesgo,
        "probabilidad": round(prob * 100, 2)
    }
