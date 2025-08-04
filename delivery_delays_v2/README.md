# 🚚 Delivery Delay Prediction API

A containerized machine learning API for predicting delivery delays using XGBoost, built with FastAPI and Docker. This project demonstrates a full end-to-end ML workflow from preprocessing to deployment.

---

## 🔧 Features

- FastAPI REST API for real-time delivery delay predictions
- Input validation using Pydantic with example schema
- Machine learning model trained with XGBoost
- Preprocessing steps include feature engineering and dummy encoding
- Dockerized for easy deployment and portability

---

## 🗂️ Project Structure
```yaml
delivery_delays_v2/
├── delivery_model_package/ # Model training, validation, pipeline
├── delivery_delays_api/    # FastAPI app
├── Dockerfile
├── .dockerignore
└── requirements.txt
```

---

## 🚀 How to Run

### 🐳 With Docker

```bash
# From the root directory (delivery_delays/)
docker build -t delivery-delay-api .
docker run -p 8000:8000 delivery-delay-api
```
Visit the API docs at http://localhost:8000/docs

---

### 🧪 Example Input (POST /api/v1/predict)
```json
{
  "inputs": [
    {
      "Type": "DEBIT",
      "Days for shipment (scheduled)": 4,
      "Benefit per order": 15.0,
      ...
    }
  ]
}
```

---

## 📦 Requirements
See requirements.txt for full list. Main dependencies:
- fastapi
- xgboost
- scikit-learn
- pandas
- uvicorn
- pydantic >=2.0,<3.0

---

# 🧠 Notes
- The model pipeline is split for better version compatibility: preprocessing is saved via joblib, XGBoost is saved via .save_model()
- Designed for further extension (CI/CD, monitoring, versioned models, etc


