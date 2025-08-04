import joblib
from train_model import train_model
from sklearn.metrics import classification_report

def evaluate_model(model, X_test, y_test):
    from sklearn.metrics import classification_report

    y_pred = model.predict(X_test)
    print("✅ Evaluation Results:")
    print(classification_report(y_test, y_pred))