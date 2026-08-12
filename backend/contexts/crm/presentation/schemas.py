"""CRM API schemas."""
from pydantic import BaseModel, Field


class CreateContactRequest(BaseModel):
    email: str = Field(min_length=3, max_length=256, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    full_name: str = Field(min_length=1, max_length=128)
    company: str | None = Field(default=None, max_length=128)
    phone: str | None = Field(default=None, max_length=32)


class CreateOpportunityRequest(BaseModel):
    contact_id: str
    title: str = Field(min_length=1, max_length=256)
    amount: str = Field(min_length=1, max_length=32)
    currency: str = Field(default="USD", min_length=3, max_length=3)


class LoseOpportunityRequest(BaseModel):
    reason: str | None = Field(default=None, max_length=512)
