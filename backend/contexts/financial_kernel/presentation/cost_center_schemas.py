"""Enterprise Cost Centers API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateCostCenterRequest(BaseModel):
    code: str
    name: str
    center_type: str
    parent_id: str | None = None
    profit_center_id: str | None = None
    manager_id: str | None = None
    metadata: dict | None = None


class CreateProfitCenterRequest(BaseModel):
    code: str
    name: str
    business_unit_id: str | None = None
    metadata: dict | None = None


class CreateAllocationRequest(BaseModel):
    allocation_type: str
    source_context: str
    source_document_id: str
    cost_center_code: str
    account_code: str
    amount: float = Field(gt=0)
    currency: str = "USD"
    profit_center_code: str | None = None
    period_id: str | None = None
    description: str = ""
    idempotency_key: str | None = None


class SplitAllocationRequest(BaseModel):
    allocation_type: str
    source_context: str
    source_document_id: str
    account_code: str
    total_amount: float = Field(gt=0)
    cost_center_codes: list[str]
    weights: list[float] | None = None
    currency: str = "USD"
    period_id: str | None = None
