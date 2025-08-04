import json

def test_health(test_client):
    response = test_client.get("/api/v1/health")
    assert response.status_code == 200
    payload = response.json()
    assert "name" in payload
    assert "api_version" in payload
    assert "model_version" in payload

def test_predict_success(test_client):
    sample_input = {
        "inputs": [
            {
                "Type": "Sustainable",
                "Days for shipment (scheduled)": 4,
                "Benefit per order": 15.0,
                "Sales per customer": 400.0,
                "Category Id": 17,
                "Category Name": "Phones",
                "Customer Segment": "Consumer",
                "Department Id": 7,
                "Department Name": "Technology",
                "Latitude": 30.2672,
                "Longitude": -97.7431,
                "Market": "US",
                "Order Item Discount": 2.0,
                "Order Item Discount Rate": 0.05,
                "Order Item Product Price": 40.0,
                "Order Item Profit Ratio": 0.25,
                "Order Item Quantity": 1,
                "Sales": 38.0,
                "Order Item Total": 38.0,
                "Order Profit Per Order": 10.0,
                "Order Region": "Central",
                "Order Status": "Delivered",
                "Product Category Id": 3,
                "Product Price": 40.0,
                "order_dayofweek": 3,
                "order_month": 6,
                "is_high_discount": 0,
                "is_bulk_order": 0,
                "discount_ratio": 0.05,
                "Shipping Mode": "Standard Class",
                "is_first_class": 0
            }
        ]
    }

    response = test_client.post("/api/v1/predict", data=json.dumps(sample_input))
    assert response.status_code == 200
    result = response.json()
    assert "predictions" in result
    assert isinstance(result["predictions"], list)