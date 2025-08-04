from load_data import load_data
from preprocess import preprocess
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import joblib
import pandas as pd

def train_model():
    # Load
    df_raw = load_data()

    # Preprocess
    df = preprocess(df_raw)

    # Feature columns
    X = df.drop(columns=['delayed'])
    y = df['delayed']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, train_size=0.7, random_state=101)
    
    feature_names = X_train.columns.tolist()

    # Train model
    model = XGBClassifier()
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(
    {"model": model, "features": feature_names}, "model/delivery_model.pkl")
    
    print("✅ Model trained and saved.")

    return model, X_test, y_test