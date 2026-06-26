from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
from csv_manager import save_analysis, read_analysis

import os
import requests

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MODELLO LOCALE
# =========================
ekman_pipeline = pipeline(
    "sentiment-analysis",
    model="arpanghoshal/EkmanClassifier"
)

# =========================
# HF CONFIG
# =========================
HF_TOKEN = os.environ.get("HF_TOKEN")

API_URL = "https://router.huggingface.co/hf-inference/models/j-hartmann/emotion-english-distilroberta-base"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


# =========================
# SAFE API CALL (ROBUST)
# =========================
def ekman_api_emotion(text: str):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": text},
            timeout=8
        )

        result = response.json()

        print("HF RAW RESPONSE:", result)

        # ❌ HF error / loading
        if isinstance(result, dict):
            return {
                "emotion": None,
                "confidence": 0.0,
                "error": result.get("error", "HF error")
            }

        # ❌ empty response
        if not isinstance(result, list) or len(result) == 0:
            return {
                "emotion": None,
                "confidence": 0.0,
                "error": "Empty response"
            }

        emotions = result[0]

        # 🔥 safe max (ignore broken entries)
        valid = [
            e for e in emotions
            if isinstance(e, dict) and "label" in e and "score" in e
        ]

        if not valid:
            return {
                "emotion": None,
                "confidence": 0.0,
                "error": "Invalid emotion format"
            }

        top = max(valid, key=lambda x: x["score"])

        return {
            "emotion": top["label"],
            "confidence": float(top["score"])
        }

    except Exception as e:
        return {
            "emotion": None,
            "confidence": 0.0,
            "error": f"API failed: {str(e)}"
        }


# =========================
# INPUT
# =========================
class InputText(BaseModel):
    name: str
    surname: str
    text: str


# =========================
# ANALYZE + SAVE
# =========================
@app.post("/analyze")
def analyze(data: InputText):

    # =====================
    # LOCAL MODEL (SAFE)
    # =====================
    try:
        result_pipeline = ekman_pipeline(data.text)[0]
        emotion_pipeline = result_pipeline["label"]
        confidence_pipeline = float(result_pipeline["score"])
    except Exception as e:
        emotion_pipeline = "error"
        confidence_pipeline = 0.0
        print("Pipeline error:", e)

    # =====================
    # API MODEL (SAFE)
    # =====================
    result_api = ekman_api_emotion(data.text)

    emotion_api = result_api["emotion"] or "unavailable"
    confidence_api = float(result_api["confidence"])

    print("API RESULT:", result_api)

    # =====================
    # AGREEMENT
    # =====================
    agreement = (
        emotion_api == emotion_pipeline
        if emotion_api != "unavailable"
        else False
    )

    # =====================
    # SAVE CSV
    # =====================
    save_analysis(
        data.name,
        data.surname,
        data.text,
        emotion_pipeline,
        confidence_pipeline,
        emotion_api,
        confidence_api,
        agreement
    )

    # =====================
    # RESPONSE
    # =====================
    return {
        "emotion_pipeline": emotion_pipeline,
        "confidence_pipeline": confidence_pipeline,
        "emotion_api": emotion_api,
        "confidence_api": confidence_api,
        "agreement": agreement,
        "api_status": "ok" if result_api["emotion"] else "fallback"
    }


# =========================
# HISTORY
# =========================
@app.get("/history/{name}/{surname}")
def get_history(name: str, surname: str):
    return read_analysis(name=name, surname=surname)