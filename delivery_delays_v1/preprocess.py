from load_data import load_data
import joblib
import pandas as pd

def preprocess(df):
    # Convert date columns
    df['order_date'] = pd.to_datetime(df['order date (DateOrders)'])
    df['ship_date'] = pd.to_datetime(df['shipping date (DateOrders)'])
    
    # Create shipping duration
    df['shipping_duration'] = (df['ship_date'] - df['order_date']).dt.days
    
    # Create custom delay label
    df['delayed'] = (df['shipping_duration'] > df['Days for shipment (scheduled)']).astype(int)
    
    # Create a cleaned Shipping Mode feature
    df['Shipping Mode Clean'] = df['Shipping Mode'].replace({'First Class': 'Unreliable'})
    
    # Add a flag for potentially unreliable mode (was First Class)
    df['is_first_class'] = (df['Shipping Mode'] == 'First Class').astype(int)
    
    # Other Feature Engineering
    df['order_dayofweek'] = df['order_date'].dt.dayofweek
    df['order_month'] = df['order_date'].dt.month
    df['is_high_discount'] = (df['Order Item Discount'] > 50).astype(int)
    df['is_bulk_order'] = (df['Order Item Quantity'] > 3).astype(int)
    
    # Drop irrelevant or high-null columns
    df = df.drop(columns=['Product Description', 'Order Zipcode', 'Customer Email', 'Customer Fname', 'Customer Lname', 'Customer Password',
    'Customer Id', 'Order Id', 'Order Item Id', 'Order Item Cardprod Id', 'Product Card Id', 'Product Image', 'Product Status',
    'order date (DateOrders)', 'shipping date (DateOrders)','Days for shipping (real)', 'shipping_duration', 'Delivery Status',
    'Late_delivery_risk', 'order_date', 'ship_date', 'Customer Street', 'Customer Zipcode', 'Customer City', 'Customer State',
    'Customer Country', 'Product Name', 'Order Customer Id','Order State', 'Order City', 'Order Country', 'Shipping Mode'], axis=1)
    
    # Convert object columns to categorical or encoded numeric format
    cat_cols = df.select_dtypes(include='object').columns

    # One-hot encode (for XGBoost trained without `enable_categorical`)
    df = pd.get_dummies(df, columns=cat_cols)
    
    # Drop any remaining nulls
    df.dropna(inplace=True)
    
    print("✅ Data cleaned.")
    
    return df