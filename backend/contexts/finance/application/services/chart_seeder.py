"""Build default chart of accounts — application layer."""
from __future__ import annotations

from contexts.finance.application.constants.default_accounts import DEFAULT_ACCOUNTS
from contexts.finance.domain.aggregates.account import Account


def build_default_accounts(tenant_id: str) -> list[Account]:
    return [
        Account.create(
            tenant_id=tenant_id,
            code=code,
            name=name,
            account_type=account_type,
        )
        for code, name, account_type in DEFAULT_ACCOUNTS
    ]
