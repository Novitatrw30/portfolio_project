# preprocess.py
"""
Preprocessing and feature engineering for Credit Risk PD model.

Includes:
- Cleaning (term, emp_length, percent strings, dates)
- Feature engineering (bin_tax_liens, rare category grouping, indicators, log transforms)
- Preprocessing (imputation, scaling, OHE)

Final output: ColumnTransformer to use inside model pipeline.
"""

import re
import numpy as np
import pandas as pd
from typing import List
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# ------------------------
# 1. Feature engineering + cleaning
# ------------------------
class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.log_cols = [
            'delinq_amnt','annual_inc','revol_bal','total_bal_il',
            'total_rev_hi_lim','avg_cur_bal','bc_open_to_buy',
            'total_bal_ex_mort','max_bal_bc','tot_cur_bal',
            'total_bc_limit','total_il_high_credit_limit'
        ]
        self.rare_purposes = ['wedding', 'renewable_energy', 'educational']
        self.rare_home = ['ANY', 'OTHER', 'NONE']

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        # ---- Cleaning ----
        # term: "36 months" -> 36
        if 'term' in X.columns:
            X['term'] = (
                X['term'].astype(str)
                          .str.replace(r'\s*months', '', regex=True)
                          .replace({'nan': None})
            )
            X['term'] = pd.to_numeric(X['term'], errors='coerce')

        # emp_length: "< 1 year", "10+ years", "3 years" -> numeric
        if 'emp_length' in X.columns:
            def _map_emp(x):
                if pd.isna(x): return np.nan
                s = str(x).strip()
                if s == '< 1 year': return 0
                if s == '10+ years': return 10
                m = re.search(r'(\d+)', s)
                return int(m.group(1)) if m else np.nan
            X['emp_length'] = X['emp_length'].map(_map_emp)

        # percent-like columns: strip "%" and convert to float
        pct_cols = ['int_rate','revol_util','il_util','bc_util','all_util']
        for c in pct_cols:
            if c in X.columns:
                X[c] = (
                    X[c].astype(str)
                        .str.replace('%','',regex=False)
                        .replace({'nan': None})
                )
                X[c] = pd.to_numeric(X[c], errors='coerce')

        # credit history length: issue_d - earliest_cr_line
        if 'earliest_cr_line' in X.columns and 'issue_d' in X.columns:
            def _parse_monyear(s):
                return pd.to_datetime(s, format='%b-%Y', errors='coerce')
            ecd = X['earliest_cr_line'].apply(_parse_monyear)
            idt = X['issue_d'].apply(_parse_monyear)
            X['credit_history_length'] = (idt - ecd).dt.days // 365
            # drop raw earliest_cr_line
            X = X.drop(columns=['earliest_cr_line'])

        # ---- Feature engineering ----
        # tax liens bin
        if 'tax_liens' in X.columns:
            def bin_tax_liens(x):
                if x == 0: return "0"
                elif x == 1: return "1"
                elif x == 2: return "2"
                else: return "3+"
            X["tax_liens_bin"] = X["tax_liens"].apply(bin_tax_liens)
            X['has_tax_liens'] = (X['tax_liens'] > 0).astype(int)

        if 'delinq_amnt' in X.columns:
            X['has_delinq'] = (X['delinq_amnt'] > 0).astype(int)

        if 'tot_coll_amt' in X.columns:
            X['has_tot_coll'] = (X['tot_coll_amt'] > 0).astype(int)

        # rare categories
        if 'purpose' in X.columns:
            X['purpose'] = X['purpose'].replace(self.rare_purposes, 'other')

        if 'home_ownership' in X.columns:
            X['home_ownership'] = X['home_ownership'].replace(self.rare_home, 'OTHER')

        # log1p transform
        for col in self.log_cols:
            if col in X.columns:
                X[col] = np.log1p(X[col])

        # drop original raw columns no longer needed
        drop_cols = [c for c in ['tax_liens','tot_coll_amt'] if c in X.columns]
        if drop_cols:
            X = X.drop(columns=drop_cols)

        return X

# ------------------------
# 2. Custom imputers
# ------------------------
class PercentClipImputer(BaseEstimator, TransformerMixin):
    def __init__(self, lower_q=0.01, upper_q=0.99):
        self.lower_q = lower_q
        self.upper_q = upper_q

    def fit(self, X, y=None):
        X_df = pd.DataFrame(X)
        self.lower_ = X_df.quantile(self.lower_q)
        self.upper_ = X_df.quantile(self.upper_q)
        self.median_ = X_df.median()
        return self

    def transform(self, X):
        X_df = pd.DataFrame(X).copy()
        for col in X_df.columns:
            low = self.lower_.get(col, np.nan)
            high = self.upper_.get(col, np.nan)
            if not np.isnan(low):
                X_df[col] = X_df[col].clip(lower=low)
            if not np.isnan(high):
                X_df[col] = X_df[col].clip(upper=high)
            med = self.median_.get(col, np.nan)
            if not np.isnan(med):
                X_df[col] = X_df[col].fillna(med)
        return X_df.values

class MaxPlusOneImputer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        X_df = pd.DataFrame(X)
        self.max_ = X_df.max(skipna=True)
        return self

    def transform(self, X):
        X_df = pd.DataFrame(X).copy()
        for col in X_df.columns:
            max_val = self.max_.get(col, np.nan)
            fill_val = (max_val + 1) if not pd.isna(max_val) else 1
            X_df[col] = X_df[col].fillna(fill_val)
        return X_df.values

# ------------------------
# 3. Build ColumnTransformer
# ------------------------
def build_preprocessor(
    X: pd.DataFrame,
    median_impute: List[str],
    median_pct: List[str],
    nol_impute: List[str],
    month_since: List[str],
    cat_exclude: List[str] = None
):
    cat_exclude = cat_exclude or []

    median_cols = [c for c in median_impute if c in X.columns]
    pct_cols = [c for c in median_pct if c in X.columns]
    nol_cols = [c for c in nol_impute if c in X.columns]
    month_cols = [c for c in month_since if c in X.columns]

    cat_cols = [
        c for c in X.select_dtypes(include=['object']).columns.tolist()
        if c not in cat_exclude
    ]

    transformers = []
    if median_cols:
        median_pipe = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        transformers.append(('median_num', median_pipe, median_cols))

    if pct_cols:
        pct_pipe = Pipeline([
            ('pct', PercentClipImputer()),
            ('scaler', StandardScaler())
        ])
        transformers.append(('pct_num', pct_pipe, pct_cols))

    if nol_cols:
        nol_pipe = Pipeline([
            ('fill0', SimpleImputer(strategy='constant', fill_value=0)),
            ('scaler', StandardScaler())
        ])
        transformers.append(('nol_num', nol_pipe, nol_cols))

    if month_cols:
        month_pipe = Pipeline([
            ('maxp1', MaxPlusOneImputer()),
            ('scaler', StandardScaler())
        ])
        transformers.append(('month_num', month_pipe, month_cols))

    if cat_cols:
        cat_pipe = Pipeline([
            ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output =False))
        ])
        transformers.append(('cat', cat_pipe, cat_cols))

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder='drop',
        sparse_threshold=0
    )

    preprocessor.fit(X)
    return preprocessor