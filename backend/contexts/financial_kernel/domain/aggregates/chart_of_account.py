"""Chart of Accounts aggregate — unlimited hierarchy, configurable codes."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from contexts.financial_kernel.domain.aggregates.account_types import (
    AccountCategory,
    EnterpriseAccountType,
)
from contexts.financial_kernel.domain.services.account_type_engine import (
    allows_gl_posting,
    apply_credit_to_balance,
    apply_debit_to_balance,
    default_account_type_for_category,
    get_posting_rule,
    get_posting_rule_for_account,
    resolve_account_type,
    resolve_category_from_type,
)
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

# Re-export for backward compatibility
AccountType = EnterpriseAccountType


class TemplateSource(StrEnum):
    TENANT = "tenant"
    INDUSTRY = "industry"
    COUNTRY = "country"


class AccountStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


def category_to_account_type(category: AccountCategory) -> str:
    return default_account_type_for_category(category.value)


@dataclass(eq=False, kw_only=True)
class ChartOfAccount(AggregateRoot):
    tenant_id: str
    code: str
    name: str
    account_category: AccountCategory
    account_type: str
    account_key: str | None = None
    parent_account_id: str | None = None
    tree_id: str | None = None
    level: int = 0
    tree_path: str = ""
    display_order: int = 0
    account_group: str | None = None
    is_posting: bool = True
    balance: float = 0.0
    statistical_balance: float = 0.0
    cost_center: str | None = None
    profit_center: str | None = None
    template_source: TemplateSource = TemplateSource.TENANT
    template_key: str | None = None
    country_code: str | None = None
    currency: str | None = None
    is_control_account: bool = False
    reconciliation_required: bool = False
    tax_code: str | None = None
    budget_code: str | None = None
    status: str = AccountStatus.ACTIVE.value
    effective_date: str | None = None
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        code: str,
        name: str,
        account_category: AccountCategory | str | None = None,
        account_type: str | None = None,
        account_key: str | None = None,
        parent_account_id: str | None = None,
        tree_id: str | None = None,
        level: int = 0,
        tree_path: str = "",
        display_order: int = 0,
        account_group: str | None = None,
        is_posting: bool = True,
        template_source: TemplateSource | str = TemplateSource.TENANT,
        template_key: str | None = None,
        country_code: str | None = None,
        currency: str | None = None,
        is_control_account: bool | None = None,
        reconciliation_required: bool | None = None,
        tax_code: str | None = None,
        budget_code: str | None = None,
        status: str = AccountStatus.ACTIVE.value,
        effective_date: str | None = None,
    ) -> ChartOfAccount:
        resolved_type = resolve_account_type(
            account_type=account_type,
            account_category=account_category.value if isinstance(account_category, AccountCategory) else account_category,
        )
        category = (
            resolve_category_from_type(resolved_type)
            if account_type
            else _resolve_category(account_category=account_category, account_type=resolved_type)
        )
        rule = get_posting_rule(resolved_type)
        path = tree_path or (account_key or code)
        if parent_account_id and account_key and tree_path:
            path = tree_path
        elif parent_account_id and account_key:
            path = account_key
        source = (
            template_source
            if isinstance(template_source, TemplateSource)
            else TemplateSource(template_source)
        )
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            code=code.strip(),
            name=name.strip(),
            account_category=category,
            account_type=resolved_type,
            account_key=account_key,
            parent_account_id=parent_account_id,
            tree_id=tree_id,
            level=level,
            tree_path=path,
            display_order=display_order,
            account_group=account_group,
            is_posting=is_posting,
            template_source=source,
            template_key=template_key,
            country_code=country_code,
            currency=currency,
            is_control_account=is_control_account if is_control_account is not None else rule.is_control_account,
            reconciliation_required=(
                reconciliation_required
                if reconciliation_required is not None
                else rule.reconciliation_required
            ),
            tax_code=tax_code,
            budget_code=budget_code,
            status=status,
            effective_date=effective_date,
        )

    def accepts_gl_posting(self) -> bool:
        if self.account_category == AccountCategory.STATISTICAL:
            return False
        return allows_gl_posting(
            account_type=self.account_type,
            is_posting=self.is_posting,
            is_active=self.is_active,
            status=self.status,
        )

    def posting_rule(self) -> dict:
        return get_posting_rule_for_account(self.to_dict())

    def deactivate(self) -> None:
        self.status = AccountStatus.INACTIVE.value
        self.is_active = False

    def activate(self, effective_date: str | None = None) -> None:
        self.status = AccountStatus.ACTIVE.value
        self.is_active = True
        if effective_date:
            self.effective_date = effective_date

    def apply_debit(self, amount: float) -> None:
        if self.account_category == AccountCategory.STATISTICAL:
            self.statistical_balance = round(self.statistical_balance + amount, 2)
            return
        if not get_posting_rule(self.account_type).gl_posting_allowed:
            return
        self.balance = apply_debit_to_balance(self.account_type, self.balance, amount)

    def apply_credit(self, amount: float) -> None:
        if self.account_category == AccountCategory.STATISTICAL:
            self.statistical_balance = round(self.statistical_balance - amount, 2)
            return
        if not get_posting_rule(self.account_type).gl_posting_allowed:
            return
        self.balance = apply_credit_to_balance(self.account_type, self.balance, amount)

    def to_dict(self) -> dict:
        rule = get_posting_rule(self.account_type)
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "code": self.code,
            "name": self.name,
            "account_key": self.account_key,
            "account_category": self.account_category.value,
            "account_type": self.account_type,
            "parent_account_id": self.parent_account_id,
            "tree_id": self.tree_id,
            "level": self.level,
            "tree_path": self.tree_path,
            "display_order": self.display_order,
            "account_group": self.account_group,
            "is_posting": self.is_posting,
            "balance": self.balance,
            "statistical_balance": self.statistical_balance,
            "template_source": self.template_source.value,
            "template_key": self.template_key,
            "country_code": self.country_code,
            "currency": self.currency,
            "is_control_account": self.is_control_account,
            "reconciliation_required": self.reconciliation_required,
            "tax_code": self.tax_code,
            "budget_code": self.budget_code,
            "status": self.status,
            "effective_date": self.effective_date,
            "is_active": self.is_active,
            "posting_rule": {
                "normal_balance": rule.normal_balance,
                "gl_posting_allowed": rule.gl_posting_allowed,
                "is_contra": rule.is_contra,
                "requires_subledger": rule.requires_subledger,
                "budget_tracked": rule.budget_tracked,
                "tax_related": rule.tax_related,
            },
        }


def _resolve_category(
    *,
    account_category: AccountCategory | str | None,
    account_type: str | None,
) -> AccountCategory:
    if account_category is not None:
        return (
            account_category
            if isinstance(account_category, AccountCategory)
            else AccountCategory(account_category)
        )
    if account_type is not None:
        return resolve_category_from_type(account_type)
    raise ValueError("account_category or account_type required")
