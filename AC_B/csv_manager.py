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



    with open(
        FILE_NAME,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:


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


    with open(
        FILE_NAME,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:


        reader = csv.DictReader(file)

        results = []



        for row in reader:


            if (

                (name is None or row["Name"] == name)

                and

                (surname is None or row["Surname"] == surname)

                and

                row["agreement"] in [
                    "full",
                    "partial"
                ]

            ):


                for field in [
                    "Emotion_Pipeline",
                    "Confidence_Pipeline",
                    "Emotion_Roberta",
                    "Confidence_Roberta",
                    "Emotion_Qwen",
                    "Confidence_Qwen",
                    "emotion_gt",
                    "intensity_gt"
                ]:

                    try:

                        row[field] = json.loads(
                            row[field]
                        )

                    except:

                        row[field] = []



                results.append(row)



        return results






# ========================
# READ CSV HISTORY
def read_history(name=None, surname=None):

    if not FILE_NAME.exists():
        return []


    with open(
        FILE_NAME,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:


        reader = csv.DictReader(file)

        history = []



        for row in reader:


            if (

                (name is None or row["Name"] == name)

                and

                (surname is None or row["Surname"] == surname)

            ):


                for field in [
                    "Emotion_Pipeline",
                    "Confidence_Pipeline",
                    "Emotion_Roberta",
                    "Confidence_Roberta",
                    "Emotion_Qwen",
                    "Confidence_Qwen",
                    "emotion_gt",
                    "intensity_gt"
                ]:

                    try:

                        row[field] = json.loads(
                            row[field]
                        )

                    except:

                        row[field] = []



                history.append(row)



        return history






# ========================
# OVERWRITE CSV HISTORY
def overwrite_history(data):

    if not data:
        return

    fieldnames = list(data[0].keys())

    with open(
        FILE_NAME,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:


        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )


        writer.writeheader()

        writer.writerows(data)