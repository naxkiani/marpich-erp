"""Registered policy domains."""
from __future__ import annotations

POLICY_DOMAINS: tuple[tuple[str, str], ...] = (
    ("university", "University Policies"),
    ("hospital", "Hospital Policies"),
    ("bank", "Bank Policies"),
    ("exchange", "Exchange Policies"),
    ("tax", "Tax Policies"),
    ("construction", "Construction Policies"),
    ("government", "Government Policies"),
)

INDUSTRY_PACK_TO_DOMAIN: dict[str, str] = {
    "university": "university",
    "school": "university",
    "hospital": "hospital",
    "clinic": "hospital",
    "bank": "bank",
    "banking": "bank",
    "currency_exchange": "exchange",
    "exchange": "exchange",
    "tax_consulting": "tax",
    "accounting_firm": "tax",
    "construction": "construction",
    "government": "government",
    "municipality": "government",
}
