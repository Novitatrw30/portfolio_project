# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from model_pipeline import predict_proba, predict

app = FastAPI(
    title="Credit Risk PD Prediction API",
    description="Predict Probability of Default (PD) for loans",
    version="0.1.0"
)

# Input schema
class LoanApplication(BaseModel):
    data: List[Dict[str, Any]]

class PredictProbaResponse(BaseModel):
    probabilities: List[float]

class PredictResponse(BaseModel):
    predictions: List[int]

@app.get("/")
def read_root():
    return {"message": "Credit Risk PD Prediction API is running!"}

@app.post("/predict_proba", response_model=PredictProbaResponse)
def predict_probability(payload: LoanApplication):
    return {"probabilities": predict_proba(payload.data)}

@app.post("/predict", response_model=PredictResponse)
def predict_flag(payload: LoanApplication, threshold: float = 0.5):
    return {"predictions": predict(payload.data, threshold)}
