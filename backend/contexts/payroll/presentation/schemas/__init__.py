"""Payroll API schemas."""
from pydantic import BaseModel, Field


class CreatePayrollRunRequest(BaseModel):
    period_label: str = Field(min_length=1, max_length=64)
