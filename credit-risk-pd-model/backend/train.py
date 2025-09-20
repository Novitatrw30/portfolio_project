# train.py
"""
Training script for Credit Risk PD model on BigQuery data.
Steps:
- Load dataset from BigQuery
- Create target (PD_flag) from loan_status
- Time-based split into train/valid/test
- Build pipeline: FeatureEngineer + Preprocessor + Calibrated XGB
- Train, evaluate, and save model
"""

import os
import joblib
import pandas as pd
from google.cloud import bigquery
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
from xgboost import XGBClassifier
from preprocess import FeatureEngineer, build_preprocessor
import joblib
from sklearn.metrics import roc_auc_score, log_loss, brier_score_loss, confusion_matrix

# ------------------------
# Config
# ------------------------
PROJECT_ID = "organic-service-468707-v3"
DATASET = "credit_risk_loss"
TABLE = "accepted_loans_copy2"   # <-- cleaned table in BigQuery
MODEL_PATH = "pd_prediction_model.pkl"

# ------------------------
# 1. Load data from BigQuery
# ------------------------
client = bigquery.Client(project=PROJECT_ID)

query = f"""
SELECT *
FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
"""
df = client.query(query).to_dataframe()

print(f"✅ Loaded {df.shape[0]:,} rows and {df.shape[1]} columns from BigQuery")

# ------------------------
# 2. Create target feature
# ------------------------
pd_mapping = {
    "Charged Off": 1,
    "Default": 1,
    "Late (31-120 days)": 1,
    "Does not meet the credit policy. Status:Charged Off": 1,
    "Fully Paid": 0,
    "Current": 0,
    "Does not meet the credit policy. Status:Fully Paid": 0
}

df["PD_flag"] = df["loan_status"].map(pd_mapping)
df = df.dropna(subset=["PD_flag"]).copy()
df["PD_flag"] = df["PD_flag"].astype(int)
df = df.drop(columns=["loan_status"])  # redundant with target

# ------------------------
# 3. Time-based split
# ------------------------
# ensure issue_d is datetime
df['issue_d'] = df['issue_d'].apply(pd.to_datetime, format='%b-%Y', errors='coerce')

sub_df = df[df["issue_d"] < "2018-01-01"].copy()
test_df = df[df["issue_d"] >= "2018-01-01"].copy()

feature_cols = [c for c in df.columns if c not in ["PD_flag", "issue_d"]]

# test
y_test = test_df["PD_flag"]
X_test = test_df[feature_cols].copy()

# valid & train
valid_df = sub_df[sub_df["issue_d"] >= "2017-01-01"].copy()
train_df = sub_df[sub_df["issue_d"] < "2017-01-01"].copy()

y_train = train_df["PD_flag"]
X_train = train_df[feature_cols].copy()

y_valid = valid_df["PD_flag"]
X_valid = valid_df[feature_cols].copy()

print(f"Train: {X_train.shape}, Valid: {X_valid.shape}, Test: {X_test.shape}")

# ------------------------
# 4. Preprocessor
# ------------------------
# feature groups (already used in preprocess.py)
median_impute = ['annual_inc','tot_coll_amt','tot_cur_bal','total_bal_il',
                 'max_bal_bc','all_util','total_rev_hi_lim','avg_cur_bal',
                 'bc_open_to_buy','bc_util','tot_hi_cred_lim',
                 'total_bal_ex_mort','total_bc_limit','total_il_high_credit_limit']

median_pct = ['dti','revol_util','il_util','percent_bc_gt_75','pct_tl_nvr_dlq']

nol_impute = ['delinq_2yrs','inq_last_6mths','open_acc','pub_rec','total_acc',
              'collections_12_mths_ex_med','acc_now_delinq','open_acc_6m',
              'open_act_il','open_il_12m','open_il_24m','open_rv_12m','open_rv_24m',
              'inq_fi','total_cu_tl','inq_last_12m','acc_open_past_24mths',
              'chargeoff_within_12_mths','delinq_amnt','mort_acc',
              'num_accts_ever_120_pd','num_actv_bc_tl','num_actv_rev_tl',
              'num_bc_sats','num_bc_tl','num_il_tl','num_op_rev_tl',
              'num_rev_accts','num_rev_tl_bal_gt_0','num_sats',
              'num_tl_120dpd_2m','num_tl_30dpd','num_tl_90g_dpd_24m',
              'num_tl_op_past_12m','pub_rec_bankruptcies','tax_liens']

month_since = ['mths_since_rcnt_il','mo_sin_old_il_acct','mo_sin_old_rev_tl_op',
               'mo_sin_rcnt_rev_tl_op','mo_sin_rcnt_tl','mths_since_recent_bc',
               'mths_since_recent_inq']

# Fit feature engineer first
fe = FeatureEngineer()
X_train_fe = fe.fit_transform(X_train)

# Preprocessor
preprocessor = build_preprocessor(X_train_fe, median_impute, median_pct, nol_impute, month_since)

# Save expected features and their types
expected_features = X_train_fe.columns.tolist()
feature_dtypes = {col: str(X_train_fe[col].dtype) for col in X_train_fe.columns}
joblib.dump(expected_features, "expected_features.pkl")
joblib.dump(feature_dtypes, "feature_dtypes.pkl")

# ------------------------
# 5. Model
# ------------------------
xgb = XGBClassifier(
    random_state=42,
    n_estimators=500,
    learning_rate=0.05,
    max_depth=4,
    subsample=0.6,
    colsample_bytree=0.6,
    scale_pos_weight=len(y_train[y_train==0]) / len(y_train[y_train==1]),
    reg_lambda=0.1,
    reg_alpha=0,
    min_child_weight=5,
    gamma=0.3,
    n_jobs=-1,
    verbosity=1
)

pipeline = Pipeline([
    ("feature_engineer", fe),
    ("preprocessor", preprocessor),
    ("model", CalibratedClassifierCV(xgb, method="sigmoid", cv=3))
])

print("🚀 Training model...")
pipeline.fit(X_train, y_train)

# ------------------------
# 6. Save model
# ------------------------
joblib.dump(pipeline, MODEL_PATH)
print(f"✅ Model saved to {MODEL_PATH}")

# ------------------------
# 7. Evaluation
# ------------------------
def evaluate_split(X, y, split_name):
    y_pred_proba = pipeline.predict_proba(X)[:, 1]
    y_pred = (y_pred_proba >= 0.5).astype(int)

    auc = roc_auc_score(y, y_pred_proba)
    logloss = log_loss(y, y_pred_proba)
    brier = brier_score_loss(y, y_pred_proba)
    cm = confusion_matrix(y, y_pred)

    print(f"\n📊 {split_name} results:")
    print(f"ROC-AUC:   {auc:.3f}")
    print(f"LogLoss:   {logloss:.3f}")
    print(f"Brier:     {brier:.3f}")
    print(f"Confusion Matrix:\n{cm}")

# Evaluate on valid and test
evaluate_split(X_valid, y_valid, "Validation")
evaluate_split(X_test, y_test, "Test")