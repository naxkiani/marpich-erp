"""Inventory API schemas."""
from decimal import Decimal

from pydantic import BaseModel, Field


class UpsertStockRequest(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    quantity: Decimal = Field(ge=0)
