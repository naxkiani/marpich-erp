"""Banking Payment Platform API schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class BeneficiaryRequest(BaseModel):
    customer_id: str
    name: str
    account_number: str
    bank_code: str = ""
    branch_code: str = ""
    currency: str = "USD"
    beneficiary_type: str = "external"


class CreateTransferRequest(BaseModel):
    transfer_type: str = Field(
        ...,
        description="internal | inter_branch | bank_to_bank | bill_payment | government_payment | salary_transfer | merchant_payment | qr_payment | real_time",
    )
    source_account_id: str
    amount: float = Field(..., gt=0)
    destination_account_id: str | None = None
    beneficiary_id: str | None = None
    channel: str | None = None
    branch_id: str = ""
    destination_branch_id: str = ""
    scheduled_at: datetime | None = None
    qr_payload: str = ""
    merchant_ref: str = ""
    bill_ref: str = ""
    government_ref: str = ""
    salary_ref: str = ""
    narrative: str = ""


class ApproveTransferRequest(BaseModel):
    approver_id: str


class ScheduleTransferRequest(BaseModel):
    scheduled_at: datetime


class ExecuteTransferRequest(BaseModel):
    approver_id: str = "system"


class BulkTransferItem(BaseModel):
    amount: float = Field(..., gt=0)
    destination_account_id: str | None = None
    beneficiary_id: str | None = None
    salary_ref: str = ""
    bill_ref: str = ""
    government_ref: str = ""
    narrative: str = ""


class BulkTransferRequest(BaseModel):
    source_account_id: str
    transfer_type: str = "bulk"
    items: list[BulkTransferItem] = Field(..., min_length=1)


class StandingOrderRequest(BaseModel):
    source_account_id: str
    transfer_type: str = "internal"
    amount: float = Field(..., gt=0)
    frequency: str = Field(..., description="daily | weekly | monthly")
    destination_account_id: str | None = None
    beneficiary_id: str | None = None
