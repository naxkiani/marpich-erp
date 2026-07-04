"""Chart of Accounts aggregate — unlimited hierarchy, configurable codes."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class AccountCategory(StrEnum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"
    OFF_BALANCE = "off_balance"
    STATISTICAL = "statistical"


class AccountType(StrEnum):
    """Legacy posting-normal balance type for standard GL categories."""

    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class TemplateSource(StrEnum):
    TENANT = "tenant"
    INDUSTRY = "industry"
    COUNTRY = "country"


_CATEGORY_TO_TYPE: dict[AccountCategory, AccountType | None] = {
    AccountCategory.ASSET: AccountType.ASSET,
    AccountCategory.LIABILITY: AccountType.LIABILITY,
    AccountCategory.EQUITY: AccountType.EQUITY,
    AccountCategory.REVENUE: AccountType.REVENUE,
    AccountCategory.EXPENSE: AccountType.EXPENSE,
    AccountCategory.OFF_BALANCE: None,
    AccountCategory.STATISTICAL: None,
}


def category_to_account_type(category: AccountCategory) -> AccountType | None:
    return _CATEGORY_TO_TYPE.get(category)


@dataclass(eq=False, kw_only=True)
class ChartOfAccount(AggregateRoot):
    tenant_id: str
    code: str
    name: str
    account_category: AccountCategory
    account_type: AccountType | None = None
    account_key: str | None = None
    parent_account_id: str | None = None
    level: int = 0
    tree_path: str = ""
    account_group: str | None = None
    is_posting: bool = True
    balance: float = 0.0
    statistical_balance: float = 0.0
    cost_center: str | None = None
    profit_center: str | None = None
    template_source: TemplateSource = TemplateSource.TENANT
    template_key: str | None = None
    country_code: str | None = None
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
        account_type: AccountType | str | None = None,
        account_key: str | None = None,
        parent_account_id: str | None = None,
        level: int = 0,
        tree_path: str = "",
        account_group: str | None = None,
        is_posting: bool = True,
        template_source: TemplateSource | str = TemplateSource.TENANT,
        template_key: str | None = None,
        country_code: str | None = None,
    ) -> ChartOfAccount:
        category = _resolve_category(account_category=account_category, account_type=account_type)
        atype = category_to_account_type(category)
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
            account_type=atype,
            account_key=account_key,
            parent_account_id=parent_account_id,
            level=level,
            tree_path=path,
            account_group=account_group,
            is_posting=is_posting,
            template_source=source,
            template_key=template_key,
            country_code=country_code,
        )

    def accepts_gl_posting(self) -> bool:
        if not self.is_posting or not self.is_active:
            return False
        return self.account_category not in (
            AccountCategory.OFF_BALANCE,
            AccountCategory.STATISTICAL,
        )

    def apply_debit(self, amount: float) -> None:
        if self.account_category == AccountCategory.STATISTICAL:
            self.statistical_balance = round(self.statistical_balance + amount, 2)
            return
        if self.account_category == AccountCategory.OFF_BALANCE:
            return
        if self.account_category in (AccountCategory.ASSET, AccountCategory.EXPENSE):
            self.balance = round(self.balance + amount, 2)
        else:
            self.balance = round(self.balance - amount, 2)

    def apply_credit(self, amount: float) -> None:
        if self.account_category == AccountCategory.STATISTICAL:
            self.statistical_balance = round(self.statistical_balance - amount, 2)
            return
        if self.account_category == AccountCategory.OFF_BALANCE:
            return
        if self.account_category in (AccountCategory.ASSET, AccountCategory.EXPENSE):
            self.balance = round(self.balance - amount, 2)
        else:
            self.balance = round(self.balance + amount, 2)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "code": self.code,
            "name": self.name,
            "account_key": self.account_key,
            "account_category": self.account_category.value,
            "account_type": self.account_type.value if self.account_type else None,
            "parent_account_id": self.parent_account_id,
            "level": self.level,
            "tree_path": self.tree_path,
            "account_group": self.account_group,
            "is_posting": self.is_posting,
            "balance": self.balance,
            "statistical_balance": self.statistical_balance,
            "template_source": self.template_source.value,
            "template_key": self.template_key,
            "country_code": self.country_code,
            "is_active": self.is_active,
        }


def _resolve_category(
    *,
    account_category: AccountCategory | str | None,
    account_type: AccountType | str | None,
) -> AccountCategory:
    if account_category is not None:
        return (
            account_category
            if isinstance(account_category, AccountCategory)
            else AccountCategory(account_category)
        )
    if account_type is not None:
        atype = account_type if isinstance(account_type, AccountType) else AccountType(account_type)
        return AccountCategory(atype.value)
    raise ValueError("account_category or account_type required")
