import pandas as pd
import joblib
from delivery_model_package.delivery_model.config.core import FEATURE_PATH
from delivery_model_package.delivery_model.config.core import config

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()   
    df['order_date'] = pd.to_datetime(df['order date (DateOrders)'])
    df['ship_date'] = pd.to_datetime(df['shipping date (DateOrders)'])
    df['shipping_duration'] = (df['ship_date'] - df['order_date']).dt.days
    df['delayed'] = (df['shipping_duration'] > df['Days for shipment (scheduled)']).astype(int)
    df['Shipping Mode Clean'] = df['Shipping Mode'].replace({'First Class': 'Unreliable'})
    df['is_first_class'] = (df['Shipping Mode'] == 'First Class').astype(int)
    df['order_dayofweek'] = df['order_date'].dt.dayofweek
    df['order_month'] = df['order_date'].dt.month
    df['is_high_discount'] = (df['Order Item Discount'] > 50).astype(int)
    df['discount_ratio'] = df['Order Item Discount'] / (df['Product Price'] + 1e-5)
    df['is_bulk_order'] = (df['Order Item Quantity'] > 3).astype(int)

    df = df.drop(columns=[
        'Product Description', 'Order Zipcode', 'Customer Email', 'Customer Fname', 'Customer Lname',
        'Customer Password', 'Customer Id', 'Order Id', 'Order Item Id', 'Order Item Cardprod Id',
        'Product Card Id', 'Product Image', 'Product Status', 'order date (DateOrders)',
        'shipping date (DateOrders)', 'Days for shipping (real)', 'shipping_duration', 'Delivery Status',
        'Late_delivery_risk', 'order_date', 'ship_date', 'Customer Street', 'Customer Zipcode',
        'Customer City', 'Customer State', 'Customer Country', 'Product Name', 'Order Customer Id',
        'Order State', 'Order City', 'Order Country', 'Shipping Mode'
    ], errors='ignore')

    df = pd.get_dummies(df, columns=df.select_dtypes(include='object').columns)

    # Load expected features from training
    if FEATURE_PATH.exists():
        expected_features = joblib.load(FEATURE_PATH)

        # Add any missing columns from training as 0
        missing_cols = [col for col in expected_features if col not in df.columns]
        df[missing_cols] = 0

        # Drop any unexpected columns (like new unseen dummies)
        df = df[expected_features]
    else:
        expected_features = df.columns  # fallback if training phase

    df.dropna(inplace=True)
    return df