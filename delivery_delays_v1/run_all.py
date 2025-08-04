from train_model import train_model
from evaluate import evaluate_model

# 🔁 One training step
model, X_test, y_test = train_model()

# 🧠 Reuse it for evaluation
evaluate_model(model, X_test, y_test)