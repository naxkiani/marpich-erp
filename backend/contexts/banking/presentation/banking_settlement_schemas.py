"""Banking Settlement Engine API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class SettlementItemRequest(BaseModel):
    source_ref: str = ""
    amount: float = Field(..., gt=0)
    counterparty: str = ""
    narrative: str = ""


class CreateSettlementBatchRequest(BaseModel):
    settlement_type: str = Field(
        ...,
        description="internal_settlement | interbank_settlement | clearing",
    )
    currency: str = "USD"
    items: list[SettlementItemRequest] = Field(..., min_length=1)


class CreateReconciliationRequest(BaseModel):
    settlement_account: str = ""
    statement_items: list[dict] = Field(default_factory=list)
    book_items: list[dict] = Field(default_factory=list)
    use_completed_transfers: bool = False


class RaiseExceptionRequest(BaseModel):
    source_type: str = Field(..., description="batch | reconciliation")
    source_id: str
    reason: str


class CreateAdjustmentRequest(BaseModel):
    run_id: str
    amount: float
    currency: str = "USD"
    reason: str = ""


class ApproveAdjustmentRequest(BaseModel):
    approver_id: str


class ApproveReconciliationRequest(BaseModel):
    approver_id: str


class GenerateReportRequest(BaseModel):
    report_type: str = "settlement_summary"
