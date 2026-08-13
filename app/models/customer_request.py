from app.database import Base
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict, EmailStr
from CustomerRequestCreate import CustomerRequestRead


class CustomerRequest(Base):
    __tablename__ = "customer_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, required=True)
    customer_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    requester_name: Mapped[str] = mapped_column(String(100), nullable=False)
    requester_email: Mapped[str] = mapped_column(String(255), nullable=False)
    request_text: Mapped[str] = mapped_column(Text, nullable=False)
    urgency: Mapped[str] = mapped_column(String(20), default="medium")
    model_config = ConfigDict(from_attributes=True)


class CustomerRequestRead(CustomerRequestCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)