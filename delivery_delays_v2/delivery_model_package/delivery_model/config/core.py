from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel
from strictyaml import YAML, Map, Str, Seq, load
from strictyaml import Optional as YAML_Optional

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
FEATURE_PATH = PACKAGE_ROOT / "expected_features.pkl"
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "datasets"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"

schema = Map({
    "package_name": Str(),
    "training_data_file": Str(),
    "test_data_file": Str(),
    "pipeline_save_file": Str(),
    "target": Str(),
    YAML_Optional("features"): Seq(Str()),
    "test_size": Str(),
    "random_state": Str(),
    "categorical_vars": Seq(Str()),
})
class AppConfig(BaseModel):
    """Application-level config."""
    package_name: str
    training_data_file: str
    test_data_file: str
    pipeline_save_file: str


class ModelConfig(BaseModel):
    target: str
    features: Optional[List[str]] = None
    test_size: float
    random_state: int

    categorical_vars_with_na_frequent: Optional[List[str]] = []
    categorical_vars_with_na_missing: Optional[List[str]] = []
    numerical_vars_with_na: Optional[List[str]] = []
    categorical_vars: List[str]

class MasterConfig(BaseModel):
    """Master config object."""
    app: AppConfig
    model: ModelConfig


def find_config_file() -> Path:
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise FileNotFoundError(f"Config file not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Optional[Path] = None) -> YAML:
    if not cfg_path:
        cfg_path = CONFIG_FILE_PATH

    with open(cfg_path, "r") as conf_file:
        return load(conf_file.read(), schema)

def create_and_validate_config(parsed_config: YAML = None) -> MasterConfig:
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    return MasterConfig(
        app=AppConfig(**parsed_config.data),
        model=ModelConfig(**parsed_config.data),
    )

config = create_and_validate_config()