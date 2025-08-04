from typing import List, Optional
import pandas as pd
from typing import Optional
from pydantic import BaseModel, ValidationError, Field
from delivery_model_package.delivery_model.config.core import config
from delivery_model_package.delivery_model.processing.data_manager import load_pipeline

class DeliveryDataInputSchema(BaseModel):
    Type: Optional[str]
    Days_for_shipping_real: Optional[int] = Field(None, alias="Days for shipping (real)")
    Days_for_shipment_scheduled: Optional[int] = Field(None, alias="Days for shipment (scheduled)")
    Benefit_per_order: Optional[float] = Field(None, alias="Benefit per order")
    Sales_per_customer: Optional[float] = Field(None, alias="Sales per customer")
    Category_Id: Optional[int] = Field(None, alias="Category Id")
    Category_Name: Optional[str] = Field(None, alias="Category Name")
    Customer_Segment: Optional[str] = Field(None, alias="Customer Segment")
    Department_Id: Optional[int] = Field(None, alias="Department Id")
    Department_Name: Optional[str] = Field(None, alias="Department Name")
    Latitude: Optional[float]
    Longitude: Optional[float]
    Market: Optional[str]
    order_date_DateOrders: Optional[str] = Field(None, alias="order date (DateOrders)")
    shipping_date_DateOrders: Optional[str] = Field(None, alias="shipping date (DateOrders)")
    Order_Item_Discount: Optional[float] = Field(None, alias="Order Item Discount")
    Order_Item_Discount_Rate: Optional[float] = Field(None, alias="Order Item Discount Rate")
    Order_Item_Product_Price: Optional[float] = Field(None, alias="Order Item Product Price")
    Order_Item_Profit_Ratio: Optional[float] = Field(None, alias="Order Item Profit Ratio")
    Order_Item_Quantity: Optional[int] = Field(None, alias="Order Item Quantity")
    Sales: Optional[float]
    Order_Item_Total: Optional[float] = Field(None, alias="Order Item Total")
    Order_Profit_Per_Order: Optional[float] = Field(None, alias="Order Profit Per Order")
    Order_Region: Optional[str] = Field(None, alias="Order Region")
    Order_Status: Optional[str] = Field(None, alias="Order Status")
    Product_Category_Id: Optional[int] = Field(None, alias="Product Category Id")
    Product_Price: Optional[float] = Field(None, alias="Product Price")
    Shipping_Mode: Optional[str] = Field(None, alias="Shipping Mode")

    class Config:
        validate_by_name = True
        validate_by_alias = True

class MultipleDeliveryDataInputs(BaseModel):
    inputs: List[DeliveryDataInputSchema]

def validate_inputs(input_data: pd.DataFrame) -> dict:
    # Optional: replace column names to match Pydantic schema keys if needed
    validated_data = input_data.copy()
    
    # Pydantic expects camelCase or snake_case keys matching the schema
    try:
        # This will raise ValidationError if data is not valid
        MultipleDeliveryDataInputs(inputs=validated_data.to_dict(orient="records"))
        return {"validated_data": validated_data, "errors": None}
    except ValidationError as error:
        return {"validated_data": None, "errors": error.json()}