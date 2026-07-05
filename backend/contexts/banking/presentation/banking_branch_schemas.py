"""Branch Banking Platform API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateOfficeRequest(BaseModel):
    office_type: str = Field(
        ...,
        description="head_office | regional_office | branch | sub_branch",
    )
    name: str
    code: str
    parent_office_id: str | None = None
    region: str = ""
    address: str = ""
    currency: str = "USD"


class AddExtensionRequest(BaseModel):
    extension_type: str = Field(
        ...,
        description="cash_counter | atm_extension | self_service_kiosk_extension",
    )
    label: str
    terminal_id: str = ""


class OpenBranchRequest(BaseModel):
    operator_id: str
    opening_balance: float = 0.0
    notes: str = ""


class CloseBranchRequest(BaseModel):
    operator_id: str
    closing_balance: float = 0.0
    notes: str = ""


class VaultMovementRequest(BaseModel):
    movement_type: str = Field(
        ...,
        description="deposit | withdrawal | transfer_to_drawer | transfer_from_drawer",
    )
    amount: float = Field(..., gt=0)
    operator_id: str = ""
    narrative: str = ""


class CashLimitRequest(BaseModel):
    limit_type: str = "drawer"
    max_amount: float = Field(..., gt=0)
    currency: str = "USD"
    extension_id: str | None = None


class EmployeeAssignmentRequest(BaseModel):
    employee_id: str
    role: str
    extension_id: str | None = None


class RecordKPIRequest(BaseModel):
    metric_key: str
    metric_value: float
    target_value: float = 0.0
    period: str = "daily"
