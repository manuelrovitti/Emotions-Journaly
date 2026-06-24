from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
from csv_manager import save_analysis, read_analysis

import pandas as pd
from pathlib import Path

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODELLO AI
ekman_pipeline = pipeline(
    "sentiment-analysis",
    model="arpanghoshal/EkmanClassifier"
)

# CSV path
DATA_FILE = Path("data/dataset.csv")

# INPUT
class InputText(BaseModel):
    name: str
    surname: str
    text: str


# =========================
# ANALYZE + SAVE
# =========================
@app.post("/analyze")
def analyze(data: InputText):

    result = ekman_pipeline(data.text)[0]

    emotion = result["label"]
    confidence = float(result["score"])

    save_analysis(
        data.name,
        data.surname,
        data.text,
        emotion,
        confidence
    )

    return {
        "emotion": emotion,
        "confidence": confidence
    }

@app.get("/history/{name}/{surname}")
def get_history(name: str, surname: str):
    return read_analysis(name=name, surname=surname)
