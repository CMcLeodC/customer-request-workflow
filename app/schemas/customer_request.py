from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr

RequestStatus = Literal[
    "new",
    "reviewing",
    "approved",
    "in_progress",
    "completed",
    "rejected",
]


class CustomerRequestCreate(BaseModel):
    customer_id: str
    requester_name: str
    requester_email: EmailStr
    request_text: str
    urgency: Literal["low", "medium", "high", "critical"] = "medium"


class CustomerRequestRead(CustomerRequestCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
    status: RequestStatus


class CustomerRequestStatusUpdate(BaseModel):
    status: RequestStatus