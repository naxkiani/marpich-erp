"""Finance API schemas."""
from pydantic import BaseModel, Field


class OpenFiscalPeriodRequest(BaseModel):
    name: str = Field(min_length=2, max_length=64)
    start_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    end_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")


class CreateAccountRequest(BaseModel):
    code: str = Field(min_length=3, max_length=16)
    name: str = Field(min_length=2, max_length=128)
    account_type: str = Field(pattern=r"^(asset|liability|equity|revenue|expense)$")
