"""Sales API schemas."""
from pydantic import BaseModel, Field


class CreateQuotationRequest(BaseModel):
    contact_id: str
    title: str = Field(min_length=1, max_length=256)
    amount: str = Field(min_length=1, max_length=32)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    opportunity_id: str | None = None
