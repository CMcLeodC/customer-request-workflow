from app.database import Base
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class RequestAnalysis(Base):
    __tablename__ = "request_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_request_id: Mapped[int] = mapped_column(
        ForeignKey("customer_requests.id"),
        unique=True,
        nullable=False,
        index=True,
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    suggested_urgency: Mapped[str] = mapped_column(String(20), nullable=False)
    implementation_notes: Mapped[str] = mapped_column(Text, nullable=False)