"""Enterprise Cash Reconciliation API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CashCountRequest(BaseModel):
    location_id: str
    counted_amount: float
    closing_type: str = "cash_closing"
    notes: str | None = None


class ShiftClosingRequest(BaseModel):
    location_id: str
    counted_amount: float
    notes: str | None = None


class BranchLocationCount(BaseModel):
    location_id: str
    counted_amount: float
    notes: str | None = None


class BranchClosingRequest(BaseModel):
    branch_id: str
    location_counts: list[BranchLocationCount] = Field(min_length=1)


class RejectVarianceRequest(BaseModel):
    reason: str = ""
