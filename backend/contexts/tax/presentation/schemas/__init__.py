"""Tax API schemas."""
from pydantic import BaseModel, Field


class FileTaxReturnRequest(BaseModel):
    period_label: str = Field(min_length=1, max_length=64)
