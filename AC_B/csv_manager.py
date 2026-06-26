import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

FILE_NAME = DATA_DIR / "dataset.csv"


def save_analysis(name, surname, text, emotion_pipeline, confidence_pipeline, emotion_api, confidence_api, agreement, gt=""):

    file_exists = FILE_NAME.exists()

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Name",
                "Surname",
                "Text",
                "Emotion_Pipeline",
                "Confidence_Pipeline",
                "Emotion_API",
                "Confidence_API",
                "agreement",
                "G_T"
            ])

        writer.writerow([
            name,
            surname,
            text,
            emotion_pipeline,
            confidence_pipeline,
            emotion_api,
            confidence_api,
            agreement,
            gt
        ])

def read_analysis(name=None, surname=None):
    if not FILE_NAME.exists():
        return []

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        results = []

        for row in reader:
            if (name is None or row["Name"] == name) and (surname is None or row["Surname"] == surname):
                results.append(row["Emotion"])

        return results