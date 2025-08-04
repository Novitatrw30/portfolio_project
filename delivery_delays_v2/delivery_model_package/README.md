# Delivery Model

A reusable machine learning package to predict delivery delays based on e-commerce shipping data.

## Features

- Automated preprocessing
- XGBoost classification model
- Config-driven pipeline
- Model serialization with `joblib`
- Reusable prediction API

## Installation

```bash
pip install -e .
```

## Usage

```python
from delivery_model.predict import make_prediction

input_data = {...}
result = make_prediction(input_data)
```

## Author
```yaml
Novita Triwidianingsih
Let me know if you want to add badges, project screenshots, or Streamlit/FastAPI instructions later!
```
