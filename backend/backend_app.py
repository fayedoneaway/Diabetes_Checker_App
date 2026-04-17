from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "logreg_3feature.pkl")

model = joblib.load(model_path)


class Input(BaseModel):
    bmi: float
    age: float
    glucose: float
    symptoms: list[str] | None = None

@app.get("/")
def home():
    return {"Welcome to the Diabetes Checker App."}

SYMPTOMS = {"a": "Frequent Urination",
            "b": "Sudden loss of weight",
            "c": "Increased thirst or hunger",
            "d": "Nausea and Vomiting",
            "e": "Blurry Vision",
                "f": "Urinary Tract Infection"}

SYMPTOM_KEYWORDS = {
    "a": ["urine", "urination", "pee", "frequent"],
    "b": ["weight", "loss", "thin", "sudden"],
    "c": ["thirst", "hunger", "hungry", "thirsty", "increase", "increased"],
    "d": ["nausea", "vomit", "vomiting"],
    "e": ["blurry", "vision", "blur"],
    "f": ["uti", "infection", "urinary"]
}

URGENT = {"a", "b", "c"}

def normalize(text: str) -> list[str]:
    text = text.lower()
    table = str.maketrans(",.!?;:", "      ")
    text = text.translate(table)
    return text.split()

def match_symptom(text: str):
    tokens = normalize(text)
    matches = []

    for code, keywords in SYMPTOM_KEYWORDS.items():
        for token in tokens:
            if token in keywords:
                matches.append(code)

    return matches

@app.get("/symptoms")
def get_symptoms():
    return {
        "choices": SYMPTOMS}

@app.get("/urgent")
def get_urgent():
    return {"Typical": list(URGENT)}

@app.post("/predict/diabetes")
def predict(data: Input):

    df = pd.DataFrame([[data.bmi, data.age, data.glucose]],
        columns=["BMI", "Age", "Glucose"])

    matched = []
    if data.symptoms:
        for s in data.symptoms:
            matched.extend(match_symptom(s))

    matched = list(set(matched))

    if URGENT.issubset(set(matched)) and data.age <= 21:
        return {
            "prediction: Possible Type 1 Diabetes. Consult doctor immediately.",
            "model confidence": "90%."
        }

    if len(matched) >= 2 and data.age >= 22:
        probs = model.predict_proba(df)[0]
        prediction = model.predict(df)[0]

        label = "High diabetes risk" if prediction == 1 else "Low diabetes risk"
        confidence_pct = f"{max(probs) * 100:.0f}%"

        return {"Prediction": label,
                "Model Confidence": f"The model is {confidence_pct} confident based on BMI, age, and glucose."
}
    return {"error": "Not enough symptoms to run prediction."}

