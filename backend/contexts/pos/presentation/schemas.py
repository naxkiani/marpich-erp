"""POS API schemas."""
from decimal import Decimal

from pydantic import BaseModel, Field


class RegisterTerminalRequest(BaseModel):
    terminal_code: str = Field(min_length=2, max_length=32)
    store_name: str = Field(min_length=1, max_length=128)


class OpenShiftRequest(BaseModel):
    terminal_id: str
    cashier_name: str = Field(min_length=1, max_length=128)


class SaleItemRequest(BaseModel):
    sku: str
    name: str
    quantity: int = Field(ge=1)
    unit_price: Decimal = Field(gt=0)


class CompleteSaleRequest(BaseModel):
    shift_id: str
    items: list[SaleItemRequest]
    subtotal: Decimal = Field(gt=0)
    tax: Decimal = Field(ge=0)
    payment_method: str = Field(min_length=1, max_length=32)
    issue_receipt: bool = True
