from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
from csv_manager import save_analysis, read_analysis, read_history

import os
import requests
from collections import Counter

app = FastAPI()

# =========================
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MODELLO LOCALE
ekman_pipeline = pipeline(
    "sentiment-analysis",
    model="arpanghoshal/EkmanClassifier"
)

# =========================
# HF CONFIG
HF_TOKEN = os.environ.get("HF_TOKEN")
EMOTIONS = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]

ROBERTA_URL = "https://router.huggingface.co/hf-inference/models/j-hartmann/emotion-english-distilroberta-base"
LLM_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


# =========================
# ROBERTA
def roberta_api_emotion(text: str):
    try:
        response = requests.post(
            ROBERTA_URL,
            headers=HEADERS,
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
            }

        # ❌ empty response
        if not isinstance(result, list) or len(result) == 0:
            return {
                "emotion": None,
                "confidence": 0.0,
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
        }

#==========================
# API QWEN  
def qwen_api_emotion(text:str):
    try:
        responce = requests.post(
            LLM_URL,
            headers = HEADERS,
            json= {
                "model" : "Qwen/Qwen2.5-7B-Instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": f"""Return only one emotion: joy, sadness, anger, fearr, surprise, disgust, neutral. Text: {text}"""
 
                    }
                ],
                "temperature":0.0
            },
            timeout=10
        )
        emotion = responce.json()["choices"][0]["message"]["content"]

        return {
            "emotion": clean_emotion(emotion),
            "confidence": 0.0,
        }

    except Exception as e:
        return {
            "emotion": None,
            "confidence": 0.0,
        }

#==========================
# CLEAN OUTPUT QWEN
def clean_emotion(text: str):
    text = text.lower()
    for e in EMOTIONS:
        if e in text:
            return e
    return "All"

#==========================
# AGREEMENT
def aggrement (emo1:str, emo2:str, emo3:str):
    emotions = [emo1, emo2, emo3]
    count = Counter(emotions)
    most_common, freq = count.most_common(1)[0]

    if freq == 3:
        return "full"
    elif freq == 2:
        return "partial"
    else:
        return "none"


# =========================
# INPUT
class InputText(BaseModel):
    name: str
    surname: str
    text: str

# =========================
# ANALYZE + SAVE
@app.post("/analyze")
def analyze(data: InputText):

    # =====================
    # LOCAL MODEL 
    try:
        result_pipeline = ekman_pipeline(data.text)[0]
        emotion_pipeline = result_pipeline["label"]
        confidence_pipeline = float(result_pipeline["score"])
    except Exception as e:
        emotion_pipeline = "error"
        confidence_pipeline = 0.0

    # =====================
    # API RROBERTA
    result_roberta = roberta_api_emotion(data.text)
    emotion_roberta = result_roberta["emotion"] or "unavailable"
    confidence_roberta = float(result_roberta["confidence"])
    print("\n ROBERTA RESULT:", result_roberta)

    #======================
    # API QWEN
    result_qwen = qwen_api_emotion(data.text)
    emotion_qwen = result_qwen["emotion"]
    print("\n QWEN RESULT:", result_qwen)


    # =====================
    # AGREEMENT
    agreement = aggrement(emotion_pipeline, emotion_roberta, emotion_qwen)

    # =====================
    # SAVE CSV
    # =====================
    save_analysis(
        data.name,
        data.surname,
        data.text,
        emotion_pipeline,
        confidence_pipeline,
        emotion_roberta,
        confidence_roberta,
        emotion_qwen,
        agreement
    )

    # =====================
    # RESPONSE
    # =====================
    return {
        "emotion_pipeline": emotion_pipeline,
        "confidence_pipeline": confidence_pipeline,
        "emotion_roberta": emotion_roberta,
        "confidence_roberta": confidence_roberta,
        "emotion_qwen": emotion_qwen,
        "agreement": agreement,
    }


# =========================
# HISTORY
# =========================
@app.get("/dashboard/{name}/{surname}")
def get_dashboaard(name: str, surname: str):
    return read_analysis(name=name, surname=surname)

@app.get("/history/{name}/{surname}")
def get_history(name:str, surname:str):
    return read_history(name=name, surname=surname)