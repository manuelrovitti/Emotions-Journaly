import uuid
import csv
import json
import ast
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
    "Confidence_Qwen",
    "agreement",
    "emotion_gt",
    "intensity_gt"
]



# ========================
# SAVE ANALYSIS CSV
def save_analysis(
    name,
    surname,
    text,
    emotions_pipeline,
    confidences_pipeline,
    emotions_roberta,
    confidences_roberta,
    emotions_qwen,
    confidences_qwen,
    agreement,
    emotion_gt,
    intensity_gt

):


    file_exists = FILE_NAME.exists()

    new_id = str(uuid.uuid4())



    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(FIELDNAMES)

        writer.writerow([
            new_id,
            name,
            surname,
            text,
            # PIPELINE
            json.dumps(
                emotions_pipeline,
                ensure_ascii=False
            ),
            json.dumps(
                confidences_pipeline,
                ensure_ascii=False
            ),
            # ROBERTA
            json.dumps(
                emotions_roberta,
                ensure_ascii=False
            ),
            json.dumps(
                confidences_roberta,
                ensure_ascii=False
            ),
            # QWEN
            json.dumps(
                emotions_qwen,
                ensure_ascii=False
            ),
            json.dumps(
                confidences_qwen,
                ensure_ascii=False
            ),
            agreement,
            # HUMAN GT
            json.dumps(
                emotion_gt,
                ensure_ascii=False
            ),
            json.dumps(
                intensity_gt,
                ensure_ascii=False
            )

        ])


# ========================
# READ CSV DASHBOARD
def read_analysis(name=None, surname=None):

    if not FILE_NAME.exists():
        return []

    with open( FILE_NAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        results = []

        for row in reader:
            if ((name is None or row["Name"] == name) and (surname is None or row["Surname"] == surname)):
                #print("AGREEMENT CSV:", repr(row["agreement"]))
                emo_agreement = ast.literal_eval(row["agreement"])
                try:
                    top_emotion = max(emo_agreement, key=emo_agreement.get)
                    #print(top_emotion)
                except:
                    top_emotion = []

                results.append(top_emotion)
    return results


# ========================
# READ CSV HISTORY
def read_history(name=None, surname=None):

    if not FILE_NAME.exists():
        return []


    with open(FILE_NAME,"r",newline="",encoding="utf-8") as file:
        reader = csv.DictReader(file)
        history = []

        for row in reader:
            if ((name is None or row["Name"] == name) and (surname is None or row["Surname"] == surname)):
                
                try:
                    data = row
                except:
                    data = []
                history.append(data)
        return history
