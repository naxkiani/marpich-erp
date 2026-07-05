"""Treasury platform engine — catalog and POS boundary helpers."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.treasury_platform import (
    EVENT_GL_RULE_MAP,
    TREASURY_PLATFORM_CATALOG,
    TreasuryCapability,
)


def list_platform_catalog() -> list[dict]:
    return [
        {
            "capability": key,
            **meta,
            "kernel_satellite": True,
            "treasury_not_pos": True,
            "gl_owner": "financial_kernel",
        }
        for key, meta in TREASURY_PLATFORM_CATALOG.items()
    ]


def list_gl_rule_map() -> dict[str, str]:
    return dict(EVENT_GL_RULE_MAP)


def pos_boundary_statement() -> dict:
    return {
        "treasury": "enterprise_liquidity",
        "pos": "retail_cash_register",
        "integration": "pos.settlement.ready → treasury account credit → kernel GL post",
        "never_merge": True,
    }


def capability_count() -> int:
    return len(TreasuryCapability)
