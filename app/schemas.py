from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ShippingRequest(BaseModel):
    origin_pincode: str = Field(..., example="110001")
    destination_pincode: str = Field(..., example="400001")
    weight: float = Field(..., example=2.5)
    length: float = Field(..., example=10)
    width: float = Field(..., example=10)
    height: float = Field(..., example=10)

class CourierRate(BaseModel):
    courier: str
    price: float
    eta_days: Optional[int] = None
    remarks: Optional[str] = None

class ShippingResponse(BaseModel):
    origin: str
    destination: str
    results: List[CourierRate]
