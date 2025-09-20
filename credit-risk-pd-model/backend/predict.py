# predict.py
"""
Local tester for PD prediction model.
- Loads model_pipeline.py
- Reads sample JSON/CSV
- Prints probabilities and predictions
"""

import json
import argparse
import pandas as pd
from model_pipeline import predict_proba, predict

def main():
    parser = argparse.ArgumentParser(description="Run PD predictions locally")
    parser.add_argument("--input", type=str, required=True,
                        help="Path to JSON or CSV file with loan data")
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="Classification threshold (default=0.5)")
    args = parser.parse_args()

    # Load input
    if args.input.endswith(".json"):
        with open(args.input, "r") as f:
            instances = json.load(f)
        if isinstance(instances, dict):
            instances = [instances]  # wrap single row
    elif args.input.endswith(".csv"):
        df = pd.read_csv(args.input)
        instances = df.to_dict(orient="records")
    else:
        raise ValueError("Input must be JSON or CSV")

    # Predict
    probs = predict_proba(instances)
    preds = predict(instances, threshold=args.threshold)

    # Output
    for i, row in enumerate(instances):
        print(f"\nRow {i+1}")
        print("Input:", row)
        print(f"PD probability: {probs[i]:.4f}")
        print(f"PD flag (>{args.threshold}): {preds[i]}")

if __name__ == "__main__":
    main()
