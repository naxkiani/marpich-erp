"""Enterprise account type engine — posting rules and validation."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.account_types import (
    ACCOUNT_TYPE_POSTING_RULES,
    AccountPostingRule,
    EnterpriseAccountType,
    NormalBalance,
)
from contexts.financial_kernel.domain.aggregates.account_types import AccountCategory


def get_posting_rule(account_type: str) -> AccountPostingRule:
    rule = ACCOUNT_TYPE_POSTING_RULES.get(account_type)
    if not rule:
        raise KeyError(f"unknown_account_type:{account_type}")
    return rule


def list_account_types() -> list[dict]:
    return [
        {
            "account_type": rule.account_type,
            "category": rule.category,
            "normal_balance": rule.normal_balance,
            "gl_posting_allowed": rule.gl_posting_allowed,
            "is_contra": rule.is_contra,
            "is_control_account": rule.is_control_account,
            "reconciliation_required": rule.reconciliation_required,
            "requires_subledger": rule.requires_subledger,
            "budget_tracked": rule.budget_tracked,
            "tax_related": rule.tax_related,
            "description": rule.description,
        }
        for rule in ACCOUNT_TYPE_POSTING_RULES.values()
    ]


def resolve_category_from_type(account_type: str) -> AccountCategory:
    rule = get_posting_rule(account_type)
    return AccountCategory(rule.category)


def default_account_type_for_category(category: str) -> str:
    mapping = {
        AccountCategory.ASSET.value: EnterpriseAccountType.ASSET.value,
        AccountCategory.LIABILITY.value: EnterpriseAccountType.LIABILITY.value,
        AccountCategory.EQUITY.value: EnterpriseAccountType.EQUITY.value,
        AccountCategory.REVENUE.value: EnterpriseAccountType.REVENUE.value,
        AccountCategory.EXPENSE.value: EnterpriseAccountType.EXPENSE.value,
        AccountCategory.OFF_BALANCE.value: EnterpriseAccountType.MEMORANDUM.value,
        AccountCategory.STATISTICAL.value: EnterpriseAccountType.MEMORANDUM.value,
    }
    return mapping.get(category, EnterpriseAccountType.ASSET.value)


def resolve_account_type(
    *,
    account_type: str | None,
    account_category: str | None,
) -> str:
    if account_type:
        get_posting_rule(account_type)  # validate
        return account_type
    if account_category:
        return default_account_type_for_category(account_category)
    raise ValueError("account_type or account_category required")


def allows_gl_posting(
    *,
    account_type: str,
    is_posting: bool,
    is_active: bool,
    status: str,
) -> bool:
    if not is_posting or not is_active or status != "active":
        return False
    rule = get_posting_rule(account_type)
    return rule.gl_posting_allowed


def apply_debit_to_balance(account_type: str, balance: float, amount: float) -> float:
    rule = get_posting_rule(account_type)
    if rule.normal_balance == NormalBalance.DEBIT.value:
        return round(balance + amount, 2)
    return round(balance - amount, 2)


def apply_credit_to_balance(account_type: str, balance: float, amount: float) -> float:
    rule = get_posting_rule(account_type)
    if rule.normal_balance == NormalBalance.CREDIT.value:
        return round(balance + amount, 2)
    return round(balance - amount, 2)


def default_flags_for_type(account_type: str) -> dict:
    rule = get_posting_rule(account_type)
    return {
        "is_control_account": rule.is_control_account,
        "reconciliation_required": rule.reconciliation_required,
        "budget_tracked": rule.budget_tracked,
        "tax_related": rule.tax_related,
    }


def validate_account_type_assignment(
    *,
    account_type: str,
    account_category: str,
    is_posting: bool,
) -> tuple[bool, str | None]:
    try:
        rule = get_posting_rule(account_type)
    except KeyError:
        return False, "unknown_account_type"
    if rule.category != account_category:
        return False, "type_category_mismatch"
    if is_posting and not rule.gl_posting_allowed:
        return False, "type_not_postable"
    return True, None


def get_posting_rule_for_account(account_dict: dict) -> dict:
    account_type = account_dict.get("account_type") or default_account_type_for_category(
        account_dict.get("account_category", "asset")
    )
    rule = get_posting_rule(account_type)
    return {
        "account_type": account_type,
        **{
            "category": rule.category,
            "normal_balance": rule.normal_balance,
            "gl_posting_allowed": rule.gl_posting_allowed,
            "is_contra": rule.is_contra,
            "is_control_account": rule.is_control_account,
            "reconciliation_required": rule.reconciliation_required,
            "requires_subledger": rule.requires_subledger,
            "budget_tracked": rule.budget_tracked,
            "tax_related": rule.tax_related,
        },
    }
