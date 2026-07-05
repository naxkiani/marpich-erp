"""Enterprise account types and posting rule definitions."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AccountCategory(StrEnum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"
    OFF_BALANCE = "off_balance"
    STATISTICAL = "statistical"


class EnterpriseAccountType(StrEnum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"
    CONTRA_ASSET = "contra_asset"
    CONTRA_LIABILITY = "contra_liability"
    CONTRA_REVENUE = "contra_revenue"
    CONTRA_EXPENSE = "contra_expense"
    MEMORANDUM = "memorandum"
    SUSPENSE = "suspense"
    CONTROL = "control"
    BANK = "bank"
    CASH = "cash"
    TAX = "tax"
    PAYROLL = "payroll"
    PROJECT = "project"
    GRANT = "grant"
    STUDENT = "student"
    PATIENT = "patient"
    CUSTOMER = "customer"
    VENDOR = "vendor"


class NormalBalance(StrEnum):
    DEBIT = "debit"
    CREDIT = "credit"


@dataclass(frozen=True, slots=True)
class AccountPostingRule:
    account_type: str
    category: str
    normal_balance: str
    gl_posting_allowed: bool
    is_contra: bool = False
    is_control_account: bool = False
    reconciliation_required: bool = False
    requires_subledger: bool = False
    budget_tracked: bool = False
    tax_related: bool = False
    description: str = ""


# Configurable posting rules — tenant policy engine may override per tenant
ACCOUNT_TYPE_POSTING_RULES: dict[str, AccountPostingRule] = {
    EnterpriseAccountType.ASSET.value: AccountPostingRule(
        account_type="asset",
        category="asset",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        description="Standard asset account",
    ),
    EnterpriseAccountType.LIABILITY.value: AccountPostingRule(
        account_type="liability",
        category="liability",
        normal_balance=NormalBalance.CREDIT.value,
        gl_posting_allowed=True,
        description="Standard liability account",
    ),
    EnterpriseAccountType.EQUITY.value: AccountPostingRule(
        account_type="equity",
        category="equity",
        normal_balance=NormalBalance.CREDIT.value,
        gl_posting_allowed=True,
        description="Standard equity account",
    ),
    EnterpriseAccountType.REVENUE.value: AccountPostingRule(
        account_type="revenue",
        category="revenue",
        normal_balance=NormalBalance.CREDIT.value,
        gl_posting_allowed=True,
        description="Standard revenue account",
    ),
    EnterpriseAccountType.EXPENSE.value: AccountPostingRule(
        account_type="expense",
        category="expense",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        budget_tracked=True,
        description="Standard expense account",
    ),
    EnterpriseAccountType.CONTRA_ASSET.value: AccountPostingRule(
        account_type="contra_asset",
        category="asset",
        normal_balance=NormalBalance.CREDIT.value,
        gl_posting_allowed=True,
        is_contra=True,
        description="Contra asset — accumulated depreciation, allowances",
    ),
    EnterpriseAccountType.CONTRA_LIABILITY.value: AccountPostingRule(
        account_type="contra_liability",
        category="liability",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        is_contra=True,
        description="Contra liability — discounts on debt",
    ),
    EnterpriseAccountType.CONTRA_REVENUE.value: AccountPostingRule(
        account_type="contra_revenue",
        category="revenue",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        is_contra=True,
        description="Contra revenue — sales returns and allowances",
    ),
    EnterpriseAccountType.CONTRA_EXPENSE.value: AccountPostingRule(
        account_type="contra_expense",
        category="expense",
        normal_balance=NormalBalance.CREDIT.value,
        gl_posting_allowed=True,
        is_contra=True,
        budget_tracked=True,
        description="Contra expense — credits to expense accounts",
    ),
    EnterpriseAccountType.MEMORANDUM.value: AccountPostingRule(
        account_type="memorandum",
        category="off_balance",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=False,
        description="Memorandum / off-balance sheet",
    ),
    EnterpriseAccountType.SUSPENSE.value: AccountPostingRule(
        account_type="suspense",
        category="asset",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        description="Suspense — temporary clearing account",
    ),
    EnterpriseAccountType.CONTROL.value: AccountPostingRule(
        account_type="control",
        category="asset",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        is_control_account=True,
        requires_subledger=True,
        description="Control account — subledger roll-up",
    ),
    EnterpriseAccountType.BANK.value: AccountPostingRule(
        account_type="bank",
        category="asset",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        is_control_account=True,
        reconciliation_required=True,
        requires_subledger=True,
        description="Bank account",
    ),
    EnterpriseAccountType.CASH.value: AccountPostingRule(
        account_type="cash",
        category="asset",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        reconciliation_required=True,
        description="Cash on hand / petty cash",
    ),
    EnterpriseAccountType.TAX.value: AccountPostingRule(
        account_type="tax",
        category="liability",
        normal_balance=NormalBalance.CREDIT.value,
        gl_posting_allowed=True,
        tax_related=True,
        description="Tax payable / receivable",
    ),
    EnterpriseAccountType.PAYROLL.value: AccountPostingRule(
        account_type="payroll",
        category="expense",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        budget_tracked=True,
        requires_subledger=True,
        description="Payroll expense / liability clearing",
    ),
    EnterpriseAccountType.PROJECT.value: AccountPostingRule(
        account_type="project",
        category="expense",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        budget_tracked=True,
        description="Project / job cost account",
    ),
    EnterpriseAccountType.GRANT.value: AccountPostingRule(
        account_type="grant",
        category="revenue",
        normal_balance=NormalBalance.CREDIT.value,
        gl_posting_allowed=True,
        budget_tracked=True,
        description="Grant revenue / restricted funds",
    ),
    EnterpriseAccountType.STUDENT.value: AccountPostingRule(
        account_type="student",
        category="asset",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        requires_subledger=True,
        description="Student receivable / deposit",
    ),
    EnterpriseAccountType.PATIENT.value: AccountPostingRule(
        account_type="patient",
        category="asset",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        requires_subledger=True,
        description="Patient receivable",
    ),
    EnterpriseAccountType.CUSTOMER.value: AccountPostingRule(
        account_type="customer",
        category="asset",
        normal_balance=NormalBalance.DEBIT.value,
        gl_posting_allowed=True,
        is_control_account=True,
        requires_subledger=True,
        reconciliation_required=True,
        description="Customer / AR control",
    ),
    EnterpriseAccountType.VENDOR.value: AccountPostingRule(
        account_type="vendor",
        category="liability",
        normal_balance=NormalBalance.CREDIT.value,
        gl_posting_allowed=True,
        is_control_account=True,
        requires_subledger=True,
        reconciliation_required=True,
        description="Vendor / AP control",
    ),
}


# Legacy alias — base GL types map to themselves
AccountType = EnterpriseAccountType
