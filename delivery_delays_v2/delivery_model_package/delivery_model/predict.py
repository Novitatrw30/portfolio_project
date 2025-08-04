import pandas as pd
import typing as t
import pickle
from delivery_model_package.delivery_model.__version__ import __version__ as _version
from delivery_model_package.delivery_model.config.core import FEATURE_PATH
from delivery_model_package.delivery_model.config.core import config
from delivery_model_package.delivery_model.processing.data_manager import load_pipeline
from delivery_model_package.delivery_model.processing.preprocessor import preprocess

MODEL_FILENAME = f"{config.app.pipeline_save_file}.pkl"
_model_pipeline = load_pipeline(file_name=MODEL_FILENAME)


def make_prediction(input_data: t.Union[pd.DataFrame, dict]) -> dict:
    """Make predictions using the saved pipeline."""

    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])

    # Run preprocessing logic (reusable)
    data_cleaned = preprocess(input_data)

    results = {
        "predictions": _model_pipeline.predict(data_cleaned).tolist(),
        "version": _version,
        "errors": None
    }

    return results