from typing import Literal

from pydantic import BaseModel, ConfigDict

RequestCategory = Literal[
    "bug",
    "feature_request",
    "access_request",
    "integration",
    "support",
    "other",
]


class RequestAnalysisRead(BaseModel):
    id: int
    customer_request_id: int
    summary: str
    category: RequestCategory
    suggested_urgency: Literal["low", "medium", "high", "critical"]
    implementation_notes: str

    model_config = ConfigDict(from_attributes=True)