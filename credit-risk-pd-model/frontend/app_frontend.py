# app_frontend.py
import streamlit as st
import pandas as pd
import requests

# Cloud Run API URL
API_URL = "https://credit-risk-pd-backend-262802289960.asia-southeast2.run.app"

st.title("📊 Credit Risk Probability of Default (PD) Prediction")

# --- Explanation ---
st.markdown("""
This app predicts the **Probability of Default (PD)** for loan applications.

- **1 = Default (High Risk)**
- **0 = Non-Default (Low Risk)**

Upload a CSV file with loan applications to get predictions.
You will receive:
- The **predicted label (0 or 1)**
- The **probability of default**
""")

# --- File uploader ---
uploaded_file = st.file_uploader("📂 Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Preview of Uploaded Data")
    st.dataframe(df.head())

    # Call API for probabilities
    payload = {"data": df.to_dict(orient="records")}
    try:
        prob_response = requests.post(f"{API_URL}/predict_proba", json=payload)
        label_response = requests.post(f"{API_URL}/predict", json=payload)

        if prob_response.status_code == 200 and label_response.status_code == 200:
            probs = prob_response.json().get("probabilities", [])
            preds = label_response.json().get("predictions", [])

            df["PD_probability"] = probs
            df["PD_prediction"] = preds

            st.write("### Predictions with Probabilities")
            st.dataframe(df)

            # Option to download results
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Predictions as CSV",
                data=csv,
                file_name="predictions.csv",
                mime="text/csv",
            )
        else:
            st.error("Error calling prediction API. Check your backend service.")

    except Exception as e:
        st.error(f"API call failed: {e}")

# --- Sample file for recruiters ---
st.markdown("### 📎 Download a sample input file to try:")
sample_csv = """loan_amnt,term,int_rate,emp_length,home_ownership,grade,annual_inc,purpose,addr_state,issue_d,earliest_cr_line,fico_range_low,fico_range_high
5000,36 months,10.5%,3 years,RENT,C,55000,credit_card,CA,Dec-2016,Jan-2010,780,784
25000,60 months,22.5%,< 1 year,MORTGAGE,A,28000,small_business,FL,Dec-2016,Sep-1999,685,689
12000,36 months,16.9%,2 years,MORTGAGE,F,42000,medical,NJ,Dec-2016,Oct-2004,660,664
8000,36 months,7.9%,10+ years,OWN,D,85000,debt_consolidation,TX,Dec-2016,Nov-2009,745,749
"""
st.download_button(
    label="📂 Download Sample CSV",
    data=sample_csv,
    file_name="sample_loans.csv",
    mime="text/csv",
)