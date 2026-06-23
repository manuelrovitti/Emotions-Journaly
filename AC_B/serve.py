from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (fondamentale per Vue)
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

# INPUT
class InputText(BaseModel):
    name: str
    surname: str
    text: str

# API
@app.post("/analyze")
def analyze(data: InputText):

    result = ekman_pipeline(data.text)[0]

    return {
        "emotion": result["label"],
        "confidence": float(result["score"])
    }