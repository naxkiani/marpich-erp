"""Analytics API schemas."""
from pydantic import BaseModel, Field


class CreateAlertRequest(BaseModel):
    metric_key: str = Field(min_length=2, max_length=64)
    name: str = Field(min_length=2, max_length=128)
    threshold: int = Field(ge=0)
    operator: str = Field(default="gte", pattern=r"^(gte|lte|eq)$")
