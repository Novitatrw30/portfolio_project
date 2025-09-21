# Credit Risk PD Prediction

🔗 **Live App:** [Try the Credit Risk PD Predictor](https://credit-risk-pd-frontend-262802289960.asia-southeast2.run.app/)

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
   - Cleaned, analyzed, and engineered features

2. **Model Training**  
   - Tested multiple models: Logistic Regression, LightGBM, and XGBoost  
   - Used stratified splits and hyperparameter tuning  
   - Applied **calibration** (Platt scaling / isotonic regression) to improve probability estimates

3. **Model Evaluation**  
   - Metrics: ROC-AUC, Brier Score, Log Loss, Precision, Recall, F1  
   - Business interpretation of probability thresholds

4. **Deployment**  
   - Packaged pipeline into a Docker container  
   - Deployed API to **GCP Cloud Run** for interactive usage by stakeholders

---

## 📊 Results
The project started with **~4.5M loan application records**, which after removing duplicates and invalid rows resulted in a **clean dataset of ~2.2M rows**.  
This highlights the importance of data preprocessing in real-world credit scoring problems.

### Model Experiments

I experimented with multiple models (XGBoost, LightGBM, Logistic Regression) and techniques (Weight of Evidence encoding, Calibration).  

The **XGBoost Pipeline + Calibration** achieved the best balance between discrimination (AUC/KS) and probability accuracy (Brier/LogLoss).

| Model                           | AUC   | KS    | Gini  | Calibrated Brier | Calibrated LogLoss |
|---------------------------------|-------|-------|-------|------------------|--------------------|
| XGBoost Base                    | 0.729 | 0.331 | 0.457 | –                | –                  |
| XGBoost + WoE                   | 0.726 | 0.332 | 0.453 | –                | –                  |
| XGBoost + Calibration           | 0.704 | 0.303 | 0.409 | 0.167            | 0.417              |
| **XGBoost Pipeline + Calibration (final)** | **0.736** | **0.345** | **0.473** | **0.124** | **0.416** |
| LightGBM Base                   | 0.674 | 0.273 | 0.356 | –                | –                  |
| Logistic Regression             | 0.680 | 0.258 | 0.359 | 0.128            | 0.402              |

This shows that calibration greatly improved the model’s probability estimates, making it more reliable for credit risk decisions.   
📌 The final model (XGBoost Pipeline + Calibration) was selected for deployment.  

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
Or access the deployed app directly here:  
👉 [Credit Risk PD Frontend](https://credit-risk-pd-frontend-262802289960.asia-southeast2.run.app/)

---

## 📖 Lessons Learned

- Handling imbalanced data and extreme skew in financial features.
- Difference between raw vs calibrated probabilities in risk modeling.
- Deployment best practices with GCP + Docker + GitHub.
- Importance of model comparison before deciding the final pipeline.

---

## ✨ Next Steps

- Add interactive Streamlit dashboard for business users.
- Implement monitoring to track model drift and recalibration needs.
- Scale to handle real-time loan applications.

---

## 👩‍💻 Author
**Novita Triwidianingsih**

📫 [LinkedIn](https://www.linkedin.com/in/novitatrw94/) | 💻 [GitHub](https://github.com/Novitatrw30/portfolio_project/)
