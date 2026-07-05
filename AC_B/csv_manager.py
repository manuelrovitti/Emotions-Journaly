import uuid
import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

FILE_NAME = DATA_DIR / "dataset.csv"
FIELDNAMES = [
    "id",
    "Name",
    "Surname",
    "Text",
    "Emotion_Pipeline",
    "Confidence_Pipeline",
    "Emotion_Roberta",
    "Confidence_Roberta",
    "Emotion_Qwen",
    "agreement",
    "G_T"
]

#========================
# SAVE ANALYSIS CSV
def save_analysis(name, surname, text, emotion_pipeline, confidence_pipeline, emotion_roberta, confidence_roberta, emotion_qwen, agreement, gt=""):

    file_exists = FILE_NAME.exists()
    new_id = str(uuid.uuid4())

    
    if isinstance(gt, list):
        gt = json.dumps(gt, ensure_ascii=False)
    elif isinstance(gt, str):
        try:
            parsed = json.loads(gt)
            gt = json.dumps(parsed, ensure_ascii=False) if isinstance(parsed, list) else gt
        except:
            pass

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        
        if isinstance(gt, list):
            gt = ",".join(gt)


        if not file_exists:
            writer.writerow([
                "id",
                "Name",
                "Surname",
                "Text",
                "Emotion_Pipeline",
                "Confidence_Pipeline",
                "Emotion_Roberta",
                "Confidence_Roberta",
                "Emotion_Qwen",
                "agreement",
                "G_T"
            ])

        writer.writerow([
            new_id,
            name,
            surname,
            text,
            emotion_pipeline,
            confidence_pipeline,
            emotion_roberta,
            confidence_roberta,
            emotion_qwen,
            agreement,
            gt
        ])

#========================
# READ CSV DASHBOARD
def read_analysis(name=None, surname=None):
    if not FILE_NAME.exists():
        return []

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        results = []

        for row in reader:
            if (
                (name is None or row["Name"] == name) and
                (surname is None or row["Surname"] == surname) and
                row["agreement"] in ["full", "partial"]
            ):

                # decode GT
                if row.get("G_T"):
                    try:
                        row["G_T"] = json.loads(row["G_T"])
                    except:
                        row["G_T"] = []
                else:
                    row["G_T"] = []

                results.append(row)

        return results
    
#========================
# READ CSV HISTORY
def read_history(name=None, surname=None):
    if not FILE_NAME.exists():
        return []

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        history = []

        for row in reader:
            if (
                (name is None or row["Name"] == name) and
                (surname is None or row["Surname"] == surname)
            ):
                raw = row.get("G_T", "").strip()

                if not raw:
                    row["G_T"] = None
                else:
                    try:
                        row["G_T"] = json.loads(raw)
                    except:
                        row["G_T"] = None

                history.append(row)

        return history
    
#========================
# OVERWRITE CSV HISTORY
def overwrite_history(data):
    if not data:
        return

    fieldnames = list(data[0].keys())

    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)