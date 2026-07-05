"""Bank Account Management API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateBankRequest(BaseModel):
    code: str
    name: str
    country: str = "US"
    organization_id: str | None = None
    swift_bic: str | None = None


class CreateBranchRequest(BaseModel):
    code: str
    name: str
    organization_id: str | None = None
    address: str | None = None
    routing_number: str | None = None
    swift_bic: str | None = None


class CreateBankAccountRequest(BaseModel):
    bank_id: str
    code: str
    name: str
    account_type: str
    currency: str = "USD"
    organization_id: str | None = None
    branch_id: str | None = None
    iban: str | None = None
    swift_bic: str | None = None
    routing_number: str | None = None
    account_number: str | None = None
    virtual_account_ref: str | None = None
    gl_account_code: str | None = None
    opening_balance: float = 0.0
    require_approval: bool = True


class ApproveBankAccountRequest(BaseModel):
    workflow_instance_id: str | None = None


class AddSignatoryRequest(BaseModel):
    name: str
    role: str = "signatory"
    organization_id: str | None = None
    email: str | None = None
    authority_limit: float | None = Field(default=None, ge=0)


class AttachDocumentRequest(BaseModel):
    document_type: str
    reference: str
    organization_id: str | None = None
    file_name: str | None = None
