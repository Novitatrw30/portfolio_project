# Credit Risk PD Prediction

This project predicts the **Probability of Default (PD)** for loan applicants using machine learning.  
It was built to demonstrate both **business understanding** of credit risk and **technical skills** in model development and deployment.

---

## 🚀 Project Overview
Banks and financial institutions rely on credit risk models to minimize losses from defaults.  
In this project, I built a **Probability of Default (PD) prediction pipeline** with the following goals:

- **Business Goal:** Assess creditworthiness of borrowers and improve decision-making on loan approvals.  
- **Technical Goal:** Train, evaluate, and deploy a machine learning model on large-scale loan data.

---

## 🛠 Tech Stack
- **Python** (pandas, scikit-learn, xgboost, matplotlib, seaborn)
- **Google Cloud Platform (GCP)**: BigQuery, Vertex AI, Cloud Run
- **Docker** for containerization
- **Git & GitHub** for version control and portfolio showcase

---

## 📂 Project Workflow
1. **Data Exploration (EDA)**  
   - Loaded 2.2M+ loan records from BigQuery  
   - Cleaned, analyzed, and engineered features (e.g., WOE encoding, binning, categorical handling)

2. **Model Training**  
   - XGBoost Classifier with hyperparameter tuning  
   - Stratified K-Fold cross-validation for robust results  
   - Calibration (Platt scaling / isotonic regression) to improve probability estimates

3. **Model Evaluation**  
   - Metrics: ROC-AUC, Brier Score, Log Loss  
   - Business interpretation of probability thresholds

4. **Deployment**  
   - Packaged pipeline into a Docker container  
   - Deployed API to **GCP Cloud Run** for interactive usage by stakeholders

---

## 📊 Results
- Calibrated model improved probability accuracy (Brier score reduced by >60%).  
- ROC-AUC ~0.69 on test set, showing reasonable discrimination power.  
- API allows business users to input loan features and receive PD prediction instantly.  

---

## 🔗 How to Use
Clone the repo:  
```bash
git clone https://github.com/Novitatrw30/portfolio_project.git
cd portfolio_project
```
Run locally with Docker:
```bash
docker build -t credit-risk-pd .
docker run -p 8080:8080 credit-risk-pd
```
Access the API at:
```bash
http://localhost:8080/predict
```

---

## 📖 Lessons Learned

- Handling imbalanced data and extreme skew in financial features.
- Difference between raw vs calibrated probabilities in risk modeling.
- Deployment best practices with GCP + Docker + GitHub.

---

## ✨ Next Steps

- Add interactive Streamlit dashboard.
- Explore alternative models (LightGBM, CatBoost).
- Compare performance with survival analysis techniques.

---

## 👩‍💻 Author: Novita Triwidianingsih

📫 [LinkedIn](https://www.linkedin.com/in/novitatrw94/) | 💻 [GitHub](https://github.com/Novitatrw30/portfolio_project/)
