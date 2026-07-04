"""Treasury engine — liquidity, dashboard, forecast helpers."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.treasury_account import TreasuryAccount


def compute_liquidity(accounts: list[TreasuryAccount]) -> dict:
    by_currency: dict[str, float] = {}
    by_type: dict[str, float] = {}
    for account in accounts:
        if not account.is_active:
            continue
        by_currency[account.currency] = round(
            by_currency.get(account.currency, 0) + account.balance, 2
        )
        by_type[account.account_type] = round(
            by_type.get(account.account_type, 0) + account.balance, 2
        )
    total = round(sum(by_currency.values()), 2)
    liquid_types = {"cash", "bank", "petty_cash", "digital_wallet"}
    liquid_balance = round(
        sum(a.balance for a in accounts if a.is_active and a.account_type in liquid_types), 2
    )
    restricted_types = {"vault", "safe"}
    restricted_balance = round(
        sum(a.balance for a in accounts if a.is_active and a.account_type in restricted_types), 2
    )
    ratio = round(liquid_balance / total, 4) if total else 0.0
    return {
        "total_balance": total,
        "liquid_balance": liquid_balance,
        "restricted_balance": restricted_balance,
        "liquidity_ratio": ratio,
        "by_currency": by_currency,
        "by_account_type": by_type,
    }


def build_dashboard(
    *,
    accounts: list[TreasuryAccount],
    pending_transfers: list[dict],
    forecasts: list[dict],
    reconciliations: list[dict],
    liquidity: dict,
) -> dict:
    return {
        "summary": {
            "account_count": len([a for a in accounts if a.is_active]),
            "total_balance": liquidity["total_balance"],
            "liquid_balance": liquidity["liquid_balance"],
            "restricted_balance": liquidity["restricted_balance"],
            "liquidity_ratio": liquidity["liquidity_ratio"],
            "pending_transfers": len(pending_transfers),
            "open_reconciliations": len(
                [r for r in reconciliations if r.get("status") != "reconciled"]
            ),
        },
        "balances_by_currency": liquidity["by_currency"],
        "balances_by_type": liquidity["by_account_type"],
        "accounts": [a.to_dict() for a in accounts if a.is_active],
        "pending_transfers": pending_transfers,
        "forecasts": forecasts[:5],
        "recent_reconciliations": reconciliations[:5],
        "liquidity_analysis": liquidity,
    }
