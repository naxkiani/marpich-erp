"""GL domain engines — delegates to double-entry engines."""
from __future__ import annotations

from contexts.financial_kernel.domain.services.double_entry_posting_engine import (
    build_reversal_lines,
)
from contexts.financial_kernel.domain.services.double_entry_validation_engine import (
    validate_journal_lines,
)


def apply_multi_currency(
    lines: list[dict],
    *,
    currency: str,
    base_currency: str,
    exchange_rate: float,
    reporting_currency: str = "",
    reporting_exchange_rate: float = 1.0,
    rate_type: str = "spot",
    rate_snapshot_id: str | None = None,
) -> list[dict]:
    enriched = []
    for line in lines:
        debit = float(line.get("debit", 0))
        credit = float(line.get("credit", 0))
        enriched.append({
            **line,
            "currency": currency,
            "base_debit": round(debit * exchange_rate, 2) if debit else 0,
            "base_credit": round(credit * exchange_rate, 2) if credit else 0,
            "reporting_debit": round(debit * reporting_exchange_rate, 2) if debit else 0,
            "reporting_credit": round(credit * reporting_exchange_rate, 2) if credit else 0,
            "exchange_rate": exchange_rate,
            "reporting_exchange_rate": reporting_exchange_rate,
            "base_currency": base_currency,
            "reporting_currency": reporting_currency or base_currency,
            "rate_type": rate_type,
            "rate_snapshot_id": rate_snapshot_id,
        })
    return enriched


def compute_expense_total(lines: list[dict], account_types: dict[str, str]) -> float:
    total = 0.0
    for line in lines:
        code = line.get("account_code", "")
        if account_types.get(code) == "expense":
            total += float(line.get("debit", 0))
    return round(total, 2)
