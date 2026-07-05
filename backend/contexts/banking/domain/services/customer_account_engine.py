"""Banking Customer and Account Engine."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.banking.domain.aggregates.customer_account_engine import (
    ACCOUNT_STATUS_TRANSITIONS,
    AccountStatus,
    AccountType,
    CustomerType,
    KycStatus,
    RiskRating,
)

CUSTOMER_ACCOUNT_CATALOG: dict[str, dict] = {
    CustomerType.INDIVIDUAL.value: {"label": "Individual Customers", "supported": True},
    CustomerType.BUSINESS.value: {"label": "Business Customers", "supported": True},
    CustomerType.GOVERNMENT.value: {"label": "Government Customers", "supported": True},
    CustomerType.NGO.value: {"label": "NGO Customers", "supported": True},
    AccountType.JOINT.value: {"label": "Joint Accounts", "supported": True},
    AccountType.SAVINGS.value: {"label": "Savings Accounts", "supported": True},
    AccountType.CURRENT.value: {"label": "Current Accounts", "supported": True},
    AccountType.FIXED_DEPOSIT.value: {"label": "Fixed Deposit Accounts", "supported": True},
    AccountType.LOAN.value: {"label": "Loan Accounts", "supported": True},
    AccountType.VIRTUAL.value: {"label": "Virtual Accounts", "supported": True},
    AccountStatus.DORMANT.value: {"label": "Dormant Accounts", "status": "dormant"},
    AccountStatus.BLOCKED.value: {"label": "Blocked Accounts", "status": "blocked"},
    AccountStatus.FROZEN.value: {"label": "Frozen Accounts", "status": "frozen"},
    AccountStatus.CLOSED.value: {"label": "Closed Accounts", "status": "closed"},
    "multi_currency": {"label": "Multi-Currency", "supported": True},
    "interest_configuration": {"label": "Interest Configuration", "supported": True},
    "minimum_balance_rules": {"label": "Minimum Balance Rules", "policy_key": "retail.account.minimum_balance"},
    "overdraft_rules": {"label": "Overdraft Rules", "policy_key": "retail.overdraft.limit"},
    "account_status_workflow": {"label": "Account Status Workflow", "transitions": True},
    "kyc_status": {"label": "KYC Status", "statuses": [s.value for s in KycStatus]},
    "risk_rating": {"label": "Risk Rating", "ratings": [r.value for r in RiskRating]},
    "approval_workflow": {"label": "Approval Workflow", "supported": True},
    "kernel_integration": {"label": "Financial Kernel Integration", "required": True},
}


def list_customer_account_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in CUSTOMER_ACCOUNT_CATALOG.items()]


def list_account_status_workflow() -> list[dict]:
    return [
        {"status": status, "allowed_transitions": transitions}
        for status, transitions in ACCOUNT_STATUS_TRANSITIONS.items()
    ]


def resolve_gl_account_code(*, account_type: str, kernel_accounts: list[dict]) -> str | None:
    from contexts.banking.domain.aggregates.customer_account_engine import DEFAULT_GL_MAP

    key = DEFAULT_GL_MAP.get(account_type, "customer_deposits")
    for acct in kernel_accounts:
        if acct.get("account_key") == key or acct.get("code") == key:
            return acct.get("code") or acct.get("account_code")
    for acct in kernel_accounts:
        code = acct.get("code") or acct.get("account_code", "")
        if key.replace("_", "") in code.lower().replace("_", ""):
            return code
    return None


def check_minimum_balance(*, balance: float, minimum_balance: float) -> dict:
    compliant = balance >= minimum_balance
    return {
        "compliant": compliant,
        "balance": balance,
        "minimum_balance": minimum_balance,
        "shortfall": round(max(0, minimum_balance - balance), 2) if not compliant else 0,
    }


def check_overdraft(*, balance: float, amount: float, overdraft_enabled: bool, overdraft_limit: float) -> dict:
    if not overdraft_enabled:
        allowed = amount <= balance
        return {"allowed": allowed, "overdraft_used": 0, "reason": "overdraft_disabled" if not allowed else "ok"}
    available = balance + overdraft_limit
    allowed = amount <= available
    overdraft_used = max(0, amount - balance) if allowed else 0
    return {
        "allowed": allowed,
        "available_with_overdraft": round(available, 2),
        "overdraft_used": round(overdraft_used, 2),
    }


def build_customer_account_dashboard(
    *,
    customers: list[dict],
    accounts: list[dict],
    products: list[dict],
) -> dict:
    by_customer_type: dict[str, int] = {}
    by_account_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    by_kyc: dict[str, int] = {}
    by_risk: dict[str, int] = {}
    kernel_linked = 0
    multi_currency: set[str] = set()

    for c in customers:
        by_customer_type[c.get("customer_type", "unknown")] = (
            by_customer_type.get(c.get("customer_type", "unknown"), 0) + 1
        )
        by_kyc[c.get("kyc_status", "unknown")] = by_kyc.get(c.get("kyc_status", "unknown"), 0) + 1
        by_risk[c.get("risk_rating", "unknown")] = by_risk.get(c.get("risk_rating", "unknown"), 0) + 1

    total_balance = 0.0
    for a in accounts:
        by_account_type[a.get("account_type", "unknown")] = (
            by_account_type.get(a.get("account_type", "unknown"), 0) + 1
        )
        by_status[a.get("status", "unknown")] = by_status.get(a.get("status", "unknown"), 0) + 1
        if a.get("kernel_linked"):
            kernel_linked += 1
        multi_currency.add(a.get("currency", "USD"))
        if a.get("status") == AccountStatus.ACTIVE.value:
            total_balance += a.get("balance", 0)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "summary": {
            "customer_count": len(customers),
            "account_count": len(accounts),
            "active_accounts": by_status.get(AccountStatus.ACTIVE.value, 0),
            "pending_approval": by_status.get(AccountStatus.PENDING_APPROVAL.value, 0),
            "kernel_linked_accounts": kernel_linked,
            "product_count": len(products),
            "currency_count": len(multi_currency),
            "total_active_balance": round(total_balance, 2),
        },
        "by_customer_type": by_customer_type,
        "by_account_type": by_account_type,
        "by_account_status": by_status,
        "by_kyc_status": by_kyc,
        "by_risk_rating": by_risk,
        "currencies": sorted(multi_currency),
        "account_status_workflow": list_account_status_workflow(),
    }


def requires_approval_for_customer(*, risk_rating: str, customer_type: str) -> bool:
    if risk_rating in {RiskRating.HIGH.value, RiskRating.CRITICAL.value}:
        return True
    if customer_type in {CustomerType.GOVERNMENT.value, CustomerType.NGO.value}:
        return True
    return False
