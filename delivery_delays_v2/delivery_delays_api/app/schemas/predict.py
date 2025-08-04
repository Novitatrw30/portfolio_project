from typing import Any, List, Optional
from pydantic import BaseModel
from delivery_model_package.delivery_model.processing.validation import DeliveryDataInputSchema


class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[int]]


class MultipleDeliveryDataInputs(BaseModel):
    inputs: List[DeliveryDataInputSchema]

    class Config:
        json_schema_extra = {
            "example": {
                "inputs": [
                    {
                        "Type": "DEBIT",
                        "Days for shipping (real)":5,
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
                        "order date (DateOrders)": "1/13/2018 12:27",
                        "shipping date (DateOrders)": "1/18/2018 10:27",
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
                        "Shipping Mode": "Standard Class",
                    }
                ]
            }
        }