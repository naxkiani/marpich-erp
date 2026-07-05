"""Enterprise fiscal calendar engine — periods, close, assistant, AI checklist."""
from __future__ import annotations

from calendar import monthrange
from datetime import UTC, date, datetime

from contexts.financial_kernel.domain.aggregates.fiscal_calendar import (
    FISCAL_CLOSE_RULES,
    CloseActionType,
    CloseLevel,
    PeriodStatus,
    PeriodType,
)
from contexts.financial_kernel.domain.aggregates.fiscal_period import FiscalPeriod, FiscalYear


def get_close_rule(action_type: str) -> dict:
    rule = FISCAL_CLOSE_RULES.get(action_type)
    if not rule:
        raise KeyError(f"unknown_close_action:{action_type}")
    return rule


def validate_close_transition(*, current_status: str, action_type: str) -> tuple[bool, str]:
    if action_type == CloseActionType.REOPEN.value:
        if current_status == PeriodStatus.OPEN.value:
            return False, "period_already_open"
        return True, ""
    if current_status in (PeriodStatus.HARD_CLOSED.value, PeriodStatus.CLOSED.value):
        return False, "period_hard_closed"
    if action_type in (
        CloseActionType.SOFT_CLOSE.value,
        CloseActionType.MONTHLY_CLOSE.value,
        CloseActionType.QUARTER_CLOSE.value,
    ) and current_status == PeriodStatus.SOFT_CLOSED.value:
        return False, "period_already_soft_closed"
    return True, ""


def validate_period_for_posting(
    *,
    period_status: str,
    journal_entry_type: str = "standard",
    is_adjustment_period: bool = False,
) -> tuple[bool, str]:
    if period_status in (PeriodStatus.HARD_CLOSED.value, PeriodStatus.CLOSED.value):
        return False, "period_closed"
    if period_status == PeriodStatus.SOFT_CLOSED.value:
        if journal_entry_type in ("adjusting", "opening_balance") or is_adjustment_period:
            return True, ""
        return False, "period_soft_closed"
    return True, ""


def generate_monthly_periods(
    *,
    tenant_id: str,
    organization_id: str | None,
    branch_id: str | None,
    fiscal_year: FiscalYear,
    calendar_id: str | None,
) -> list[FiscalPeriod]:
    start = date.fromisoformat(fiscal_year.start_date)
    end = date.fromisoformat(fiscal_year.end_date)
    periods: list[FiscalPeriod] = []
    cursor = date(start.year, start.month, 1)
    number = 1
    while cursor <= end:
        last_day = monthrange(cursor.year, cursor.month)[1]
        period_end = date(cursor.year, cursor.month, last_day)
        if period_end > end:
            period_end = end
        periods.append(
            FiscalPeriod.open_period(
                tenant_id=tenant_id,
                organization_id=organization_id,
                branch_id=branch_id,
                fiscal_year_id=str(fiscal_year.id),
                calendar_id=calendar_id,
                name=f"{fiscal_year.name} P{number:02d}",
                start_date=cursor.isoformat(),
                end_date=period_end.isoformat(),
                period_type=PeriodType.MONTHLY.value,
                period_number=number,
            )
        )
        number += 1
        if cursor.month == 12:
            cursor = date(cursor.year + 1, 1, 1)
        else:
            cursor = date(cursor.year, cursor.month + 1, 1)
        if cursor > end:
            break
    return periods


def create_adjustment_period(
    *,
    tenant_id: str,
    organization_id: str | None,
    branch_id: str | None,
    fiscal_year: FiscalYear,
    calendar_id: str | None,
) -> FiscalPeriod:
    return FiscalPeriod.open_period(
        tenant_id=tenant_id,
        organization_id=organization_id,
        branch_id=branch_id,
        fiscal_year_id=str(fiscal_year.id),
        calendar_id=calendar_id,
        name=f"{fiscal_year.name} Adjustment",
        start_date=fiscal_year.end_date,
        end_date=fiscal_year.end_date,
        period_type=PeriodType.ADJUSTMENT.value,
        period_number=99,
        is_adjustment=True,
    )


def quarter_period_numbers(period_number: int) -> list[int]:
    quarter = ((period_number - 1) // 3) + 1
    start = (quarter - 1) * 3 + 1
    return [start, start + 1, start + 2]


def build_closing_assistant(
    *,
    period: dict,
    trial_balance: list[dict],
    journal_count: int,
    unposted_count: int,
) -> dict:
    total_debit = round(sum(float(r.get("debit_balance", 0)) for r in trial_balance), 2)
    total_credit = round(sum(float(r.get("credit_balance", 0)) for r in trial_balance), 2)
    balanced = total_debit == total_credit
    steps = [
        {
            "step": 1,
            "title": "Verify trial balance",
            "status": "complete" if balanced else "action_required",
            "detail": f"Debits {total_debit} / Credits {total_credit}",
        },
        {
            "step": 2,
            "title": "Clear unposted journals",
            "status": "complete" if unposted_count == 0 else "action_required",
            "detail": f"{unposted_count} draft/pending journals",
        },
        {
            "step": 3,
            "title": "Post adjusting entries",
            "status": "pending" if period.get("accepts_adjustments") else "skipped",
            "detail": "Accruals, deferrals, reclassifications",
        },
        {
            "step": 4,
            "title": "Run subledger reconciliation",
            "status": "pending",
            "detail": "AR, AP, bank, inventory control accounts",
        },
        {
            "step": 5,
            "title": "Apply soft close",
            "status": "ready" if balanced and unposted_count == 0 else "blocked",
            "detail": "Blocks new postings; adjustments still allowed",
        },
        {
            "step": 6,
            "title": "Apply hard close",
            "status": "pending",
            "detail": "Requires dual approval and financial lock",
        },
    ]
    ready = balanced and unposted_count == 0
    return {
        "period_id": period.get("id"),
        "period_name": period.get("name"),
        "period_status": period.get("status"),
        "ready_for_close": ready,
        "steps": steps,
        "summary": {
            "journal_count": journal_count,
            "unposted_count": unposted_count,
            "trial_balance_balanced": balanced,
        },
    }


def generate_ai_closing_checklist(
    *,
    period: dict,
    trial_balance: list[dict],
    journals: list[dict],
    unposted_count: int,
) -> dict:
    total_debit = round(sum(float(r.get("debit_balance", 0)) for r in trial_balance), 2)
    total_credit = round(sum(float(r.get("credit_balance", 0)) for r in trial_balance), 2)
    items: list[dict] = []

    if total_debit != total_credit:
        items.append(
            {
                "id": "tb_imbalance",
                "category": "trial_balance",
                "severity": "critical",
                "title": "Trial balance out of balance",
                "recommendation": "Investigate variance before close",
                "auto_fixable": False,
            }
        )

    if unposted_count > 0:
        items.append(
            {
                "id": "unposted_journals",
                "category": "posting",
                "severity": "high",
                "title": f"{unposted_count} unposted journals",
                "recommendation": "Post or void draft journals before soft close",
                "auto_fixable": False,
            }
        )

    large_lines = [
        j for j in journals
        if j.get("status") == "posted"
        and max(float(j.get("total_debits", 0)), float(j.get("total_credits", 0))) > 50000
    ]
    if large_lines:
        items.append(
            {
                "id": "large_entries",
                "category": "risk",
                "severity": "medium",
                "title": f"{len(large_lines)} large posted entries",
                "recommendation": "Review high-value transactions for period",
                "auto_fixable": False,
            }
        )

    if period.get("status") == PeriodStatus.SOFT_CLOSED.value:
        items.append(
            {
                "id": "soft_closed_pending_hard",
                "category": "close",
                "severity": "low",
                "title": "Period soft closed — hard close pending",
                "recommendation": "Complete adjustment entries then request hard close",
                "auto_fixable": False,
            }
        )

    if not items:
        items.append(
            {
                "id": "clear",
                "category": "status",
                "severity": "info",
                "title": "No blocking issues detected",
                "recommendation": "Proceed with close workflow",
                "auto_fixable": True,
            }
        )

    risk_score = min(1.0, sum(
        {"critical": 0.4, "high": 0.25, "medium": 0.15, "low": 0.05, "info": 0}.get(i["severity"], 0.1)
        for i in items
    ))
    return {
        "period_id": period.get("id"),
        "generated_at": datetime.now(UTC).isoformat(),
        "source": "financial_kernel.ai.closing_checklist",
        "risk_score": round(risk_score, 2),
        "recommendation": "review" if risk_score >= 0.3 else "proceed",
        "item_count": len(items),
        "items": items,
    }
