"""Municipality API schemas."""
from decimal import Decimal

from pydantic import BaseModel, Field


class ApplyPermitRequest(BaseModel):
    applicant_name: str = Field(min_length=1, max_length=128)
    permit_type: str = Field(min_length=1, max_length=64)
    description: str = Field(min_length=1, max_length=512)


class OpenServiceRequestRequest(BaseModel):
    citizen_name: str = Field(min_length=1, max_length=128)
    category: str = Field(min_length=1, max_length=64)
    description: str = Field(min_length=1, max_length=512)


class CloseServiceRequestRequest(BaseModel):
    resolution: str = Field(min_length=1, max_length=512)


class RegisterUtilityAccountRequest(BaseModel):
    account_number: str = Field(min_length=3, max_length=32)
    holder_name: str = Field(min_length=1, max_length=128)
    utility_type: str = Field(pattern=r"^(water|waste|electricity)$")


class IssueUtilityBillRequest(BaseModel):
    amount: Decimal = Field(gt=0)
    period: str = Field(min_length=1, max_length=32)
