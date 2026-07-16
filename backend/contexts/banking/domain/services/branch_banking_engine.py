"""Branch Banking Platform domain logic."""
from __future__ import annotations

from contexts.banking.domain.aggregates.branch_banking_engine import BranchOfficeType, BranchSessionStatus

BRANCH_CATALOG: dict[str, dict] = {
    "head_office": {"label": "Head Office", "supported": True},
    "regional_office": {"label": "Regional Office", "supported": True},
    "branch": {"label": "Branch", "supported": True},
    "sub_branch": {"label": "Sub Branch", "supported": True},
    "cash_counter": {"label": "Cash Counter", "supported": True},
    "atm_extension": {"label": "ATM Extension", "supported": True},
    "self_service_kiosk_extension": {"label": "Self Service Kiosk Extension", "supported": True},
    "branch_opening": {"label": "Branch Opening", "supported": True},
    "branch_closing": {"label": "Branch Closing", "supported": True},
    "vault_management": {"label": "Vault Management", "supported": True},
    "cash_limits": {"label": "Cash Limits", "supported": True},
    "employee_assignment": {"label": "Employee Assignment", "supported": True},
    "branch_kpis": {"label": "Branch KPIs", "supported": True},
    "branch_analytics": {"label": "Branch Analytics", "supported": True},
}

BRANCH_POLICY_KEYS: list[dict] = [
    {"key": "branch.cash.drawer.limit", "description": "Teller cash drawer maximum"},
    {"key": "branch.large_cash.transaction_threshold", "description": "Large cash transaction threshold"},
    {"key": "branch.opening.checklist", "description": "Branch opening checklist rules"},
    {"key": "branch.closing.checklist", "description": "Branch closing checklist rules"},
    {"key": "branch.vault.limit", "description": "Branch vault maximum balance"},
    {"key": "branch.cash.counter.limit", "description": "Cash counter transaction limits"},
    {"key": "branch.kpi.targets", "description": "Branch KPI target thresholds"},
    {"key": "branch.employee.max_assignments", "description": "Max employee assignments per branch"},
]

VALID_PARENT_TYPES: dict[str, set[str | None]] = {
    BranchOfficeType.HEAD_OFFICE.value: {None},
    BranchOfficeType.REGIONAL_OFFICE.value: {BranchOfficeType.HEAD_OFFICE.value},
    BranchOfficeType.BRANCH.value: {BranchOfficeType.REGIONAL_OFFICE.value, BranchOfficeType.HEAD_OFFICE.value},
    BranchOfficeType.SUB_BRANCH.value: {BranchOfficeType.BRANCH.value},
}


def list_branch_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in BRANCH_CATALOG.items()]


def list_branch_policy_keys() -> list[dict]:
    return list(BRANCH_POLICY_KEYS)


def validate_office_hierarchy(*, office_type: str, parent_type: str | None) -> bool:
    allowed = VALID_PARENT_TYPES.get(office_type)
    if allowed is None:
        return False
    return parent_type in allowed


def build_branch_dashboard(
    *,
    offices: list[dict],
    extensions: list[dict],
    vaults: list[dict],
    assignments: list[dict],
    kpis: list[dict],
    sessions: list[dict],
) -> dict:
    by_type: dict[str, int] = {}
    open_count = 0
    for o in offices:
        by_type[o.get("office_type", "unknown")] = by_type.get(o.get("office_type", "unknown"), 0) + 1
        if o.get("status") == BranchSessionStatus.OPEN.value:
            open_count += 1

    by_extension: dict[str, int] = {}
    for e in extensions:
        by_extension[e.get("extension_type", "unknown")] = (
            by_extension.get(e.get("extension_type", "unknown"), 0) + 1
        )

    total_vault = round(sum(float(v.get("balance", 0)) for v in vaults), 2)
    active_assignments = sum(1 for a in assignments if a.get("active"))
    opening_sessions = sum(1 for s in sessions if s.get("session_type") == "opening")
    closing_sessions = sum(1 for s in sessions if s.get("session_type") == "closing")

    kpi_summary: dict[str, dict] = {}
    for k in kpis:
        key = k.get("metric_key", "unknown")
        kpi_summary[key] = {
            "latest_value": k.get("metric_value"),
            "target": k.get("target_value"),
            "achievement_pct": k.get("achievement_pct"),
        }

    return {
        "office_count": len(offices),
        "offices_by_type": by_type,
        "open_offices": open_count,
        "extension_count": len(extensions),
        "extensions_by_type": by_extension,
        "total_vault_balance": total_vault,
        "active_assignments": active_assignments,
        "opening_sessions": opening_sessions,
        "closing_sessions": closing_sessions,
        "kpi_summary": kpi_summary,
    }


def build_branch_analytics(
    *,
    offices: list[dict],
    kpis: list[dict],
    vaults: list[dict],
    sessions: list[dict],
) -> dict:
    regional_performance: dict[str, list[dict]] = {}
    for o in offices:
        region = o.get("region") or "unassigned"
        office_kpis = [k for k in kpis if k.get("office_id") == o.get("id")]
        regional_performance.setdefault(region, []).append(
            {
                "office_ref": o.get("office_ref"),
                "office_type": o.get("office_type"),
                "status": o.get("status"),
                "kpi_count": len(office_kpis),
                "avg_achievement": _avg_achievement(office_kpis),
            }
        )

    vault_by_office = {
        v.get("office_id"): v.get("balance", 0) for v in vaults
    }

    return {
        "regions": len(regional_performance),
        "regional_performance": regional_performance,
        "vault_by_office": vault_by_office,
        "session_count": len(sessions),
        "open_rate_pct": round(
            sum(1 for o in offices if o.get("status") == "open") / len(offices) * 100, 2
        )
        if offices
        else 0.0,
    }


def _avg_achievement(kpis: list[dict]) -> float | None:
    values = [k["achievement_pct"] for k in kpis if k.get("achievement_pct") is not None]
    if not values:
        return None
    return round(sum(values) / len(values), 2)
