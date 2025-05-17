import joblib
import pandas as pd
import numpy as np
import gdown
from pathlib import Path
from app.core.config import settings
from app.models.patient import PatientInput
import os
import requests


def descargar_desde_drive(file_id, output_path):
    output_path = Path(output_path)
    if not output_path.exists():
        print(f"Descargando modelo desde Google Drive a {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, str(output_path), quiet=False)
        print(f"✅ Descargado: {output_path} ({output_path.stat().st_size / (1024**2):.2f} MB)")



def load_model():
    try:
        model_path = Path(settings.MODEL_PATH)
        descargar_desde_drive("1fX1U9rYfkBl0mWWbfSlvHv7oATpGDvvH", model_path)  # <-- coloca el ID correcto aquí
        model = joblib.load(model_path)
        return model
    except Exception as e:
        raise Exception(f"Error al cargar el modelo: {e}")


def load_model_features():
    try:
        features_path = Path(settings.MODEL_PATH)
        descargar_desde_drive("1wYmXfXB35ixMoWIUVTvisCXujjYi8lfF", features_path)  # <-- ID del segundo archivo
        features = joblib.load(features_path)
        return features
    except Exception as e:
        raise Exception(f"Error al cargar las características del modelo: {e}")


def calculate_bmi(weight_kg, height_cm):
    """Calcula el Índice de Masa Corporal
    
    Args:
        weight_kg: Peso en kilogramos
        height_cm: Altura en centímetros
    """
    height_m = height_cm / 100
    
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    """Devuelve la categoría de IMC"""
    if bmi < 18.5:
        return "Bajo peso"
    elif bmi < 25:
        return "Peso normal"
    elif bmi < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"

def get_recommendations(patient_data, prediction, bmi):
    """Genera recomendaciones personalizadas basadas en los datos del paciente"""
    recommendations = []
    
    if bmi < 18.5:
        recommendations.append("Considere aumentar su ingesta calórica y consultar con un nutricionista.")
    elif bmi >= 25 and bmi < 30:
        recommendations.append("Intente reducir ligeramente su ingesta calórica y aumentar la actividad física.")
    elif bmi >= 30:
        recommendations.append("Consulte con un profesional de la salud sobre estrategias para gestionar su peso.")
    
    if patient_data.fumador == "current":
        recommendations.append("Dejar de fumar reduciría significativamente su riesgo de hipertensión.")
    

    if patient_data.actividadFisica == "low":
        recommendations.append("Intente realizar al menos 150 minutos de actividad física moderada a la semana.")
    

    if patient_data.sueno < 6:
        recommendations.append("Procure dormir al menos 7-8 horas diarias para mejorar su salud cardiovascular.")
    elif patient_data.sueno > 9:
        recommendations.append("Dormir demasiado también puede estar asociado con problemas de salud. Consulte con su médico.")
    

    if prediction:
        recommendations.append("Es recomendable que consulte con un médico para evaluar su presión arterial.")
        recommendations.append("Reduzca el consumo de sal y lleve una dieta equilibrada rica en frutas y verduras.")
    
    return recommendations

def preprocess_input(patient: PatientInput):
    """Preprocesa los datos del paciente para que coincidan con el nuevo modelo"""

    bmi = calculate_bmi(patient.peso, patient.altura)

    data = {
        'Gender': 1 if patient.sexo == "male" else 0,
        'Age': patient.edad,
        'BMI': bmi,
        'Physical_Activity_Level': {"low": 0, "moderate": 1, "high": 2}[patient.actividadFisica],
        'Sleep_Duration': round(patient.sueno),
        'Smoking_Status': {"never": 0, "former": 1, "current": 2}[patient.fumador],
        'Family_History': 1 if patient.antecedentesHipertension == "yes" else 0
    }

    df = pd.DataFrame([data])
    return df, bmi

def predict_hypertension(patient: PatientInput):
    try:
        model_path = Path(settings.MODEL_PATH)
        
        # 🔄 Descargar el modelo si no existe
        descargar_desde_drive("1fX1U9rYfkBl0mWWbfSlvHv7oATpGDvvH", model_path)
        
        # ✅ Cargar el modelo SOLO durante la predicción
        model = joblib.load(model_path)
        
        # 📄 Descargar y cargar columnas
        features_path = model_path.parent / "model_columns.joblib"
        descargar_desde_drive("1wYmXfXB35ixMoWIUVTvisCXujjYi8lfF", features_path)
        expected_features = joblib.load(features_path)

        # 🧼 Preprocesar
        df, bmi = preprocess_input(patient)
        for col in expected_features:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_features]

        prediction = bool(model.predict(df)[0])
        probabilities = model.predict_proba(df)[0]
        probability = round(probabilities[1], 4) if prediction else round(probabilities[0], 4)

        return {
            "riesgo_hipertension": prediction,
            "probabilidad": probability
        }

    except Exception as e:
        raise Exception(f"Error al realizar la predicción: {e}")