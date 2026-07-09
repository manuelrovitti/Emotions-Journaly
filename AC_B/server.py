from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
from csv_manager import DATA_DIR, save_analysis, read_analysis, read_history, overwrite_history
from config import HF_TOKEN
#import os
import requests
import json, csv
from collections import Counter

app = FastAPI()
FILE_NAME = DATA_DIR / "dataset.csv"

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
    model="arpanghoshal/EkmanClassifier",
    top_k=3
)

#==========================
# PIPELINE
def pipeline_emotion(text: str):

    try:

        result_pipeline = ekman_pipeline(text)

        return result_pipeline[0]

    except Exception:

        return []

# =========================
# HF CONFIG
#HF_TOKEN = os.environ.get("HF_TOKEN")
EMOTIONS = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]
ROBERTA_URL = "https://router.huggingface.co/hf-inference/models/j-hartmann/emotion-english-distilroberta-base"
LLM_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

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

        #print("HF RAW RESPONSE:", result)

        if isinstance(result, dict):
            return {
                "emotion": None,
                "confidence": 0.0,
            }

        if not isinstance(result, list) or len(result) == 0:
            return {
                "emotion": None,
                "confidence": 0.0,
            }

        emotions = result[0]

        valid = [
            e for e in emotions
            if isinstance(e, dict) and "label" in e and "score" in e
        ]

        if not valid:
            return {
                "emotion": None,
                "confidence": 0.0,
            }

        #top = max(valid, key=lambda x: x["score"])
        top=valid[:3]
        #return {
        #    "emotion": top["label"][0],
        #    "confidence": float(top["score"][0])
        #}
        #print("top:", top)
        return top

    except Exception as e:
        return {
            "emotion": None,
            "confidence": 0.0,
        }

#==========================
# API QWEN  
def qwen_api_emotion(text: str):

    try:

        response = requests.post(
            LLM_URL,
            headers=HEADERS,
            json={

                "model": "Qwen/Qwen2.5-7B-Instruct",

                "messages": [
                    {
                        "role": "user",
                        "content": f"""
Analyze the emotion of this text.

Return ONLY a JSON array with the 3 most likely emotions.

Allowed emotions:
joy, sadness, anger, fear, surprise, disgust, neutral

Format:

[
  {{
    "emotion": "emotion_name",
    "confidence": 0.0
  }},
  {{
    "emotion": "emotion_name",
    "confidence": 0.0
  }},
  {{
    "emotion": "emotion_name",
    "confidence": 0.0
  }}
]

The sum of confidence values must be 1.

Text:
{text}
"""
                    }
                ],

                "temperature":0.0

            },

            timeout=10
        )


        content = response.json()["choices"][0]["message"]["content"]
        content = content.replace("```json","")
        content = content.replace("```","")
        content = content.strip()

        emotions = json.loads(content)

        return emotions

    except Exception as e:

        print("QWEN ERROR:", e)

        return [
            {
                "emotion": None,
                "confidence":0.0
            }
        ]

#==========================
# AGREEMENT
def aggrement (emo1:str, emo2:str, emo3:str):
    emotions = [emo1, emo2, emo3]
    count = Counter(emotions)
    _, freq = count.most_common(1)[0]

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

    emotion: list[str]
    intensity: list[float]

#=========================
# G_T
class GTRequest(BaseModel):
    name: str
    surname: str
    id: str
    gt: list[str]

# =========================
# ANALYZE + SAVE
@app.post("/analyze")
def analyze(data: InputText):

    #======================
    # LOCAL PIPELINE
    result_pipeline = pipeline_emotion(data.text)
    emotions_pipeline = [e["label"] for e in result_pipeline]
    confidences_pipeline = [float(e["score"])for e in result_pipeline]
    print("\n PIPELINE RESULT:", result_pipeline)
    
    # =====================
    # API RROBERTA
    result_roberta = roberta_api_emotion(data.text)
    emotions_roberta = [e["label"] for e in result_roberta]
    #emotion_roberta1 = result_roberta[0]["label"] or "unavailable"
    #emotion_roberta2 = result_roberta[1]["label"] or "unavailable"
    #emotion_roberta3 = result_roberta[2]["label"] or "unavailable"
    confidences_roberta = [e["score"] for e in result_roberta]
    #confidence_roberta1 = float(result_roberta[0]["score"])
    #confidence_roberta2 = float(result_roberta[1]["score"])
    #confidence_roberta3 = float(result_roberta[2]["score"])
    print("\n ROBERTA RESULT:", result_roberta)

    #======================
    # API QWEN
    result_qwen = qwen_api_emotion(data.text)
    emotions_qwen = [e["emotion"]for e in result_qwen]
    confidences_qwen = [float(e["confidence"])for e in result_qwen]
    print("\n QWEN RESULT:", result_qwen)

    # =====================
    # AGREEMENT
    agreement = aggrement(emotions_pipeline[0], emotions_roberta[0], emotions_qwen[0])

    # =====================
    # SAVE CSV
    save_analysis(
        data.name,
        data.surname,
        data.text,

        # MODEL OUTPUT
        emotions_pipeline,
        confidences_pipeline,

        emotions_roberta,
        confidences_roberta,

        emotions_qwen,
        confidences_qwen,

        agreement,

        # HUMAN GROUND TRUTH
        data.emotion,
        data.intensity
    )

    # =====================
    # RESPONSE
    return {

        "emotion_pipeline": emotions_pipeline,
        "confidence_pipeline": confidences_pipeline,

        "emotion_roberta": emotions_roberta[0],
        "confidence_roberta": confidences_roberta[0],

        "emotion_qwen": emotions_qwen[0],
        "confidence_qwen": confidences_qwen[0],

        "agreement": agreement,


        # HUMAN LABEL
        "emotion_gt": data.emotion,
        "intensity_gt": data.intensity

    }


# =========================
# HISTORY DASHBOARD
@app.get("/dashboard/{name}/{surname}")
def get_dashboaard(name: str, surname: str):
    return read_analysis(name=name, surname=surname)

#==========================
# HISTORY TOTAL
@app.get("/history/{name}/{surname}")
def get_history(name:str, surname:str):
    return read_history(name=name, surname=surname)

#==========================
# SAVE G_T
@app.post("/save-gt")
def save_gt(data: GTRequest):
    if not FILE_NAME.exists():
        return {"status": "error", "message": "File CSV non trovato"}
    
    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    found = False

    for row in rows:
        if row["id"] == data.id:
            row["G_T"] = json.dumps(data.gt, ensure_ascii=False)
            found = True
            break

    if not found:
        return {"status": "error", "message": "ID non trovato"}

    overwrite_history(rows)

    return {"status": "ok"}