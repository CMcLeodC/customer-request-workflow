from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerRequestCreate(BaseModel):
    customer_id: str
    requester_name: str
    requester_email: EmailStr
    request_text: str
    urgency: Literal["low", "medium", "high", "critical"] = "medium"


class CustomerRequestRead(CustomerRequestCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)