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
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── uvicorn
│
├── delivery_model_package/ # Model training, validation, pipeline
│   ├── delivery_model/			# ML folder
│   ├── pyproject.toml
│   ├── setup.cfg
│   ├── tox.ini
│   ├── requirements.txt
│   ├── README.md
│   ├── MANIFEST.in
│   ├── run_test.py
│
├── delivery_delays_api/
│   ├── requirements.txt
│   ├── tox.ini
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── __version__.py
│   │   ├── schemas/
│   │   │   └── __init__.py
│   │   │   └── health.py
│   │   │   └── predict.py
│   │   ├── tests/
│   │   │   └── __init__.py
│   │   │   └── conftest.py
│   │   │   └── test_api.py
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

## 🧠 Notes
- The model pipeline is split for better version compatibility: preprocessing is saved via joblib, XGBoost is saved via .save_model()
- Designed for further extension (CI/CD, monitoring, versioned models, etc)

---

## 📌 Author
Novita Triwidianingsih
📫 [LinkedIn](https://www.linkedin.com/in/novitatrw94/) | 💻 [GitHub](https://github.com/Novitatrw30/portfolio_project/)


