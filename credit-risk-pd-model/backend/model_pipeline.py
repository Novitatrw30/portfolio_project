# model_pipeline.py
"""
Model serving script for Credit Risk PD prediction.

Responsibilities:
- Load trained pipeline (FeatureEngineer + Preprocessor + Calibrated XGB)
- Expose predict() and predict_proba() for deployment
- Accept raw JSON/dict rows and return predictions
"""

import joblib
import pandas as pd
import numpy as np

# ------------------------
# Load model at startup
# ------------------------
MODEL_PATH = "pd_prediction_model.pkl"

print("📦 Loading model...")
model = joblib.load(MODEL_PATH)

# Load schema
expected_features = joblib.load("expected_features.pkl")
feature_dtypes = joblib.load("feature_dtypes.pkl")

print("✅ Model and Features List loaded successfully")

def prepare_input(instances: list[dict]) -> pd.DataFrame:
    """Prepare input data for prediction: align features, handle missing, enforce dtypes."""

    # Convert list of dicts → DataFrame
    df = pd.DataFrame(instances).copy()

    # 1. Keep only expected columns
    df = df[[c for c in expected_features if c in df.columns]]

    # 2. Add missing expected columns
    for col in expected_features:
        if col not in df.columns:
            if "float" in feature_dtypes[col] or "int" in feature_dtypes[col]:
                df[col] = np.nan   # numeric missing
            else:
                df[col] = "MISSING"  # categorical/text missing

    # 3. Enforce dtype consistency
    for col, dtype in feature_dtypes.items():
        if col not in df.columns:
            continue
        try:
            if "float" in dtype or "int" in dtype:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            else:
                df[col] = df[col].astype(str)
        except Exception:
            pass  # fallback if conversion fails

    # 4. Reorder columns to match training
    df = df[expected_features]

    return df

# ------------------------
# Prediction functions
# ------------------------
def predict_proba(instances):
    df = prepare_input(instances)
    probs = model.predict_proba(df)[:, 1]
    return probs.tolist()


def predict(instances, threshold=0.5):
    """
    instances: list of dicts
    threshold: cutoff for PD classification
    Returns: list of 0/1 predictions
    """
    
    proba = predict_proba(instances)
    preds = [int(p >= threshold) for p in proba]
    return preds

# ------------------------
# Example local test
# ------------------------
if __name__ == "__main__":
    # Example fake input (replace with real schema!)
    sample = [{
        "loan_amnt": 10000,
        "term": "36 months",
        "int_rate": "12.5%",
        "installment": 332.14,
        "grade": "B",
        "sub_grade": "B3",
        "emp_length": "10+ years",
        "home_ownership": "MORTGAGE",
        "annual_inc": 55000,
        "purpose": "credit_card",
        "addr_state": "CA",
        "dti": 15.3,
        "delinq_amnt": 0,
        "tot_coll_amt": 0,
        "tax_liens": 0,
        "issue_d": "2017-06-01"  # used only in training split, ignored here
    }]
    print("🔍 Probabilities:", predict_proba(sample))
    print("🔍 Predictions:", predict(sample))
