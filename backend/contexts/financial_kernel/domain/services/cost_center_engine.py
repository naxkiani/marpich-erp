"""Enterprise cost center engine — allocations and profitability."""
from __future__ import annotations


def validate_allocation_amount(amount: float) -> None:
    if amount <= 0:
        raise ValueError("invalid_allocation_amount")


def split_allocation(total: float, weights: list[float]) -> list[float]:
    if not weights or sum(weights) <= 0:
        raise ValueError("invalid_allocation_weights")
    total_w = sum(weights)
    allocated = 0.0
    parts: list[float] = []
    for i, w in enumerate(weights):
        if i < len(weights) - 1:
            part = round(total * (w / total_w), 2)
            allocated = round(allocated + part, 2)
            parts.append(part)
        else:
            parts.append(round(total - allocated, 2))
    return parts


def compute_profitability(
    *,
    journals: list[dict],
    account_types: dict[str, str],
    cost_center_code: str | None = None,
    profit_center_code: str | None = None,
) -> dict:
    revenue = 0.0
    expenses = 0.0
    budget_allocated = 0.0

    for journal in journals:
        if journal.get("status") != "posted":
            continue
        for line in journal.get("lines", []):
            cc = (line.get("cost_center") or "").upper()
            pc = (line.get("profit_center") or "").upper()
            if cost_center_code and cc != cost_center_code.upper():
                continue
            if profit_center_code and pc != profit_center_code.upper():
                continue

            code = line.get("account_code", "")
            acct_type = account_types.get(code, "")
            debit = float(line.get("debit", 0))
            credit = float(line.get("credit", 0))

            if acct_type == "revenue":
                revenue = round(revenue + credit - debit, 2)
            elif acct_type == "expense":
                expenses = round(expenses + debit - credit, 2)

    profit = round(revenue - expenses, 2)
    margin = round((profit / revenue * 100) if revenue else 0.0, 2)

    return {
        "cost_center_code": cost_center_code,
        "profit_center_code": profit_center_code,
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "margin_percent": margin,
        "budget_allocated": budget_allocated,
    }


def rollup_profitability(center_results: list[dict]) -> dict:
    revenue = round(sum(r.get("revenue", 0) for r in center_results), 2)
    expenses = round(sum(r.get("expenses", 0) for r in center_results), 2)
    profit = round(revenue - expenses, 2)
    margin = round((profit / revenue * 100) if revenue else 0.0, 2)
    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "margin_percent": margin,
        "center_count": len(center_results),
    }
