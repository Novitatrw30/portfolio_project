from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger
import numpy as np
import pandas as pd
from delivery_delays_api.app.__version__ import __version__
from delivery_delays_api.app.schemas.health import Health
from delivery_delays_api.app.schemas.predict import MultipleDeliveryDataInputs, PredictionResults
from delivery_model_package.delivery_model.__version__ import __version__ as model_version
from delivery_model_package.delivery_model.predict import make_prediction
from delivery_delays_api.app.config import settings

api_router = APIRouter()


@api_router.get("/health", response_model=Health, status_code=200)
def health() -> dict:
    """
    Root Get
    """
    health = Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )

    return health.dict()


@api_router.post("/predict", response_model=PredictionResults, status_code=200)
async def predict(
    input_data: MultipleDeliveryDataInputs
) -> dict:
    input_df = pd.DataFrame(jsonable_encoder(input_data.inputs, by_alias=True))

    try:
        logger.info(f"Making prediction on: {input_df.head().to_dict()}")
        results = make_prediction(input_data=input_df.replace({np.nan: None}))

        if results["errors"] is not None:
            logger.warning(f"Prediction error: {results['errors']}")
            raise HTTPException(status_code=400, detail=results["errors"])

        return results

    except Exception as e:
        logger.exception("Unhandled exception during prediction")
        raise HTTPException(status_code=500, detail=str(e))