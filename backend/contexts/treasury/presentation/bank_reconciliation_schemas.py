"""Enterprise Bank Reconciliation API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class StatementItemRequest(BaseModel):
    reference: str
    amount: float
    date: str = ""


class ImportStatementRequest(BaseModel):
    treasury_account_id: str
    source: str = "file_import"
    statement_date: str
    statement_balance: float
    items: list[StatementItemRequest]


class BankApiImportRequest(BaseModel):
    treasury_account_id: str
    statement_date: str
    api_payload: dict


class CreateBankReconciliationRequest(BaseModel):
    treasury_account_id: str
    reconciliation_date: str
    statement_balance: float
    statement_items: list[StatementItemRequest]
    book_items: list[StatementItemRequest] | None = None
    statement_import_id: str | None = None


class ManualMatchRequest(BaseModel):
    statement_item: dict
    book_item: dict


class RejectReconciliationRequest(BaseModel):
    reason: str = ""
