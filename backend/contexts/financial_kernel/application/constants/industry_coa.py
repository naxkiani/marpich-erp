"""Industry COA templates — delegates to YAML catalog (no hardcoded account numbers)."""
from __future__ import annotations

from contexts.financial_kernel.application.services.coa_template_loader import (
    INDUSTRY_COST_CENTERS,
    INDUSTRY_PACK_TO_COA,
    build_accounts,
    list_country_templates,
    list_industry_templates,
    materialize_template_tree,
)

__all__ = [
    "INDUSTRY_COST_CENTERS",
    "INDUSTRY_PACK_TO_COA",
    "build_accounts",
    "list_country_templates",
    "list_industry_templates",
    "materialize_template_tree",
]
