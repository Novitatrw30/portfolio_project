from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

delivery_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", XGBClassifier(random_state=101))
])