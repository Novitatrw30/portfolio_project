# 🚚 Delivery Delay Prediction with XGBoost + Streamlit Dashboard

A machine learning project that predicts whether an order will be delivered late based on a real-world supply chain dataset. Includes an automated ML pipeline and an interactive Streamlit app for live predictions.

---

## 📊 Project Overview

This project was built to solve a classification problem using the Dataco Smart Supply Chain dataset (~180K records, 50+ features). We used XGBoost for modeling and deployed an interactive dashboard using Streamlit.

---

## 🧠 Key Features

- ✅ Full pipeline: data cleaning → training → evaluation → dashboard
- ✅ Automated with modular scripts (`run_all.py`)
- ✅ Streamlit web app for real-time CSV upload & prediction
- ✅ Uses a sample CSV for deployment demo (<25MB GitHub limit)
- ✅ Ready to scale or plug into APIs, dashboards, or cron jobs

---

## 🛠️ Tech Stack

- **Python 3.10**
- **Pandas** & **NumPy**
- **Scikit-learn**
- **XGBoost**
- **Joblib** (model saving)
- **Streamlit** (interactive app)

---

## 📁 Project Structure
```yaml
delivery_delays_project/
├── data/
│ └── sample_data.csv # sample for demo
├── model/
│ └── delivery_model.pkl # trained XGBoost model
├── notebooks/
│ └── Delivery_Delays_XGBoost.ipynb
├── app.py # Streamlit app
├── run_all.py # One-click pipeline runner
├── train_model.py
├── evaluate.py
├── load_data.py
├── preprocess.py
├── requirements.txt
├── README.md
└── .streamlit/
  └── config.toml # optional layout config
```
---

## 📁 Dataset

- **Source**: [Dataco Smart Supply Chain (Kaggle)](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)  
- **Size**: 180,519 rows × 53 columns  
- **Includes**: order details, shipping info, customer & product data, geography, and sales.
- ⚠️ **Note**: This app uses a 1,000-row sample to demonstrate functionality.

---

## 🧠 How to Use

### 1. 🔁 Retrain the model (optional)

```python
python run_all.py
```

This script will:
- Load + clean the data
- Train the model
- Evaluate accuracy & F1 score
- Save the model to model/delivery_model.pkl

### 2. 🎯 Run the Streamlit App

```python
streamlit run app.py
```

Then open your browser at http://localhost:8501.
Upload a CSV with the same structure as the training data to get predictions.

---

## 🚀 How to Run the App Locally

```bash
# 1. Clone the repository
git clone https://github.com/Novitatrw30/my_portfolio.git
cd my_portfolio/delivery_delays

# 2. Install required packages
pip install -r requirements.txt  # Or install manually

# 3. Place the dataset
# Download from data folder

# 4. Run the Streamlit app
streamlit run streamlit_app.py
```
---

## 🌍 Streamlit Cloud (Demo Link)
👉 [Try the app here (hosted on Streamlit Cloud)](https://late-delivery-risk.streamlit.app/)
- Interact with the model directly in your browser. Fill in the order details to see if a delivery is predicted to be late.

---

## 📌 Project Highlights
- Conducted full EDA and handled 50+ features
- Built modular Python scripts for data loading and preprocessing
- Implemented and tuned XGBoost classifier
- Created a user-friendly web app using Streamlit
- Automated model saving and loading with joblib

## 🔄 Future Improvements
- Add cross-validation and hyperparameter tuning
- Enhance feature engineering with external data (e.g., weather, location)
- Improve model explainability using SHAP or LIME
- Deploy with Docker or on other cloud platforms

---

## 📌 Author
Novita Triwidianingsih
📫 [LinkedIn](https://www.linkedin.com/in/novitatrw94/) | 💻 [GitHub](https://github.com/Novitatrw30/my_portfolio/)
