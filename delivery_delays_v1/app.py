import pathlib        
import streamlit as st
import pandas as pd
import joblib
from preprocess import preprocess

st.set_page_config(page_title="Delivery Delay Risk Predictor", page_icon="📦")

st.title("📦 Delivery Delay Risk Predictor")
st.write(
    """
    Upload a CSV with the same columns as the training data.  
    The app will return the **Late_delivery_risk** prediction for each row.
    """
)

uploaded_file = st.file_uploader("Choose your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # 1. Load raw CSV (specify encoding if needed)
        raw_df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

        # Load model and feature list
        ROOT = pathlib.Path(__file__).parent
        MODEL_PATH = ROOT / "model" / "delivery_model.pkl"
        bundle = joblib.load(MODEL_PATH)
        model = bundle["model"]
        feature_names = bundle["features"]
       
        # 2. Apply EXACT SAME preprocessing as training
        clean_df = preprocess(raw_df.copy())

        # Reindex: add missing columns, drop extras
        clean_df = clean_df.reindex(columns=feature_names, fill_value=0)

        # 4. Predict and attach to original data
        preds = model.predict(clean_df)
        raw_df["Late_delivery_risk_pred"] = preds

        # 5. Show results
        st.success("✅ Prediction complete!")
        st.dataframe(raw_df)          # nice interactive table

        # 6. Allow user to download results
        csv = raw_df.to_csv(index=False).encode('ISO-8859-1')
        st.download_button(
            "Download predictions as CSV",
            data=csv,
            file_name="delivery_predictions.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"❌ Something went wrong:\n\n{e}")
