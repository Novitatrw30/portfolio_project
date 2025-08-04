import pandas as pd
from xgboost import XGBClassifier
from pathlib import Path
from sklearn.pipeline import Pipeline
import joblib

from delivery_model_package.delivery_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config
from delivery_model_package.delivery_model.processing.preprocessor import preprocess


def load_dataset(file_name: str) -> pd.DataFrame:
    data = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"), encoding='ISO-8859-1')
    data = preprocess(data)
    return data

def save_pipeline(pipeline_to_persist: Pipeline) -> None:
    save_file_name = f"{config.app.pipeline_save_file}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name
    joblib.dump(pipeline_to_persist, save_path)
    print(f"✅ Model saved to: {save_path}")

def load_pipeline(file_name: str) -> Pipeline:
    file_path = TRAINED_MODEL_DIR / file_name
    pipeline = joblib.load(file_path)

    # Reload the XGBoost model
    xgb_model = XGBClassifier()
    xgb_model.load_model(TRAINED_MODEL_DIR / "xgb_model.json")

    # Reattach to pipeline
    pipeline.named_steps["classifier"] = xgb_model
    return pipeline