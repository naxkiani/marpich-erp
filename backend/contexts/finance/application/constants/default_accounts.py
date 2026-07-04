"""Default chart of accounts for new tenants."""
from __future__ import annotations

from contexts.finance.domain.aggregates.account import AccountType

DEFAULT_ACCOUNTS: tuple[tuple[str, str, AccountType], ...] = (
    ("1000", "Cash", AccountType.ASSET),
    ("1200", "Accounts Receivable", AccountType.ASSET),
    ("2000", "Accounts Payable", AccountType.LIABILITY),
    ("3000", "Retained Earnings", AccountType.EQUITY),
    ("4000", "Clinical Revenue", AccountType.REVENUE),
    ("5000", "Operating Expenses", AccountType.EXPENSE),
)
