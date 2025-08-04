# 📦 Predicting Delivery Delays in a Smart Supply Chain using XGBoost

This project builds a machine learning model to predict whether an order will be delivered late using real-world supply chain data. The goal is to help businesses proactively address shipping issues, improve logistics performance, and enhance customer satisfaction.

---

## 🧠 Problem Statement

Shipping delays negatively impact customer experience and operational efficiency. This project aims to classify orders as delayed or on-time based on historical order, customer, and shipping data.

---

## 📁 Dataset

- **Source**: [Dataco Smart Supply Chain (Kaggle)](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)  
- **Size**: 180,519 rows × 53 columns  
- **Includes**: order details, shipping info, customer & product data, geography, and sales

---

## 🔍 Exploratory Data Analysis (EDA)

Key insights:
- ~57% of orders were delayed
- Standard Class shipping made up ~60% of shipments
- “First Class” had a suspicious 100% delay rate → flagged as unreliable
- Shipping delays were fairly evenly distributed throughout the year (no strong seasonality)

---

## 🛠️ Feature Engineering

Created several domain-specific features:
- `shipping_duration`: Time between order and ship dates
- `order_month`: Month of order
- `Shipping Mode Clean`: Cleaned suspicious shipping categories
- `is_first_class`: Flag for known unreliable shipping mode
- One-hot encoding of categorical variables

---

## 📈 Modeling

Used an **XGBoost Classifier** with stratified split and class balancing:

```python
XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    random_state=42,
    eval_metric='logloss',
    scale_pos_weight= len(y_train[y_train==0]) / len(y_train[y_train==1])
)
```

## 📐 Evaluation Results

### 🔹 Default Threshold (0.5)

| Class         | Precision | Recall | F1-Score |
|---------------|-----------|--------|----------|
| 0 (On time)   | 0.64      | 0.91   | 0.75     |
| 1 (Delayed)   | 0.89      | 0.57   | 0.70     |

- **Accuracy**: 73%  
- **Weighted F1-score**: 72%

---

### 🔸 Tuned Threshold (0.4)

| Class         | Precision | Recall | F1-Score |
|---------------|-----------|--------|----------|
| 0 (On time)   | 0.65      | 0.88   | 0.75     |
| 1 (Delayed)   | 0.86      | 0.60   | 0.71     |

- **Why tune the threshold?**  
  Increasing recall helps the business catch more potential delays — even with a small drop in precision. This trade-off favors **early detection** over **perfect accuracy**.

---

## 🔍 Feature Importance
Top 5 most important features based on model.feature_importances_:
1. Shipping Mode Clean – Second Class  
2. is_first_class (flag for former “First Class”)  
3. Days for shipment (scheduled)  
4. Market_USCA  
5. Order Region_North Africa

These features play a major role in predicting whether a shipment will be delayed.

---

## 💡 Business Insights
- “First Class” shipping was always delayed → likely an error or operational issue; flagged and adjusted during feature engineering
- “Second Class” also had a high delay rate (~80%), which may require business process review
- Delay pattern is not seasonal, meaning internal logistics factors are more influential than demand surges

---

## ✅ Final Summary
This project demonstrates a structured approach to predictive modeling and real-world insight:
- ✅ Cleaned and explored a large supply chain dataset
- 🧱 Built meaningful features to reflect logistics operations
- 🤖 Trained and evaluated an XGBoost model with class imbalance and threshold tuning
- 🔍 Interpreted feature importance and delivery trends
- 🎯 Derived actionable business insights

---

## 🧰 Tools Used
- Python (Pandas, NumPy, Matplotlib, Seaborn)
- Scikit-learn
- XGBoost
- Jupyter Notebook

---

## 📌 Author
Novita Triwidianingsih
📫 [LinkedIn](https://www.linkedin.com/in/novitatrw94/) | 💻 [GitHub](https://github.com/Novitatrw30/my_portfolio/)
