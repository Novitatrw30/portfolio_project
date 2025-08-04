import pandas as pd
import joblib
from config.core import FEATURE_PATH
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from delivery_model_package.delivery_model.config.core import config
from delivery_model_package.delivery_model.pipeline import delivery_pipe
from delivery_model_package.delivery_model.processing.data_manager import save_pipeline, load_dataset


def run_training() -> None:
    """Train the model and save the pipeline."""

    # Load the data
    data = load_dataset(file_name=config.app.training_data_file)
    
    # Separate target
    target = config.model.target
    X = data.drop(columns=[target])
    y = data[target]
    
    # Split into train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config.model.test_size,
        random_state=config.model.random_state
    )

    # Fit the pipeline
    delivery_pipe.fit(X_train, y_train)
    joblib.dump(X_train.columns.tolist(), FEATURE_PATH)

    # Save XGBoost model separately
    xgb_model = delivery_pipe.named_steps["classifier"]
    xgb_model.get_booster().save_model("delivery_model_package/delivery_model/trained_models/xgb_model.json")

    # Remove model before saving pipeline
    delivery_pipe.named_steps["classifier"] = None
    save_pipeline(pipeline_to_persist=delivery_pipe)

    print("✅ Model trained and saved successfully.")

if __name__ == "__main__":
    run_training()