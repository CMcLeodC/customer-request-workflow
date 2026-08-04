from pydantic import BaseModel, EmailStr
from typing import Literal


class CustomerRequestCreate(BaseModel):
    customer_id: str
    requester_name: str
    requester_email: EmailStr
    request_text: str
    urgency: Literal['low', 'medium', 'high', 'critical'] = 'medium'

