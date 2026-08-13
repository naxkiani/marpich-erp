"""Command from inventory.stock.adjusted — Pharmacy ACL (facts only)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NoteStockAdjustedCommand:
    tenant_id: str
    correlation_id: str
    sku: str
    quantity_on_hand: float
    reason: str
