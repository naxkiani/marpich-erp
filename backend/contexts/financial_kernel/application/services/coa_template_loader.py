"""Load industry and country COA templates from canonical YAML — no hardcoded account numbers."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from contexts.financial_kernel.domain.aggregates.chart_of_account import (
    AccountCategory,
    ChartOfAccount,
    TemplateSource,
)

_REPO_ROOT = Path(__file__).resolve().parents[5]
_TEMPLATE_PATH = _REPO_ROOT / "docs/architecture/financial_kernel/ACCOUNT_TREE_TEMPLATES.v1.yaml"

INDUSTRY_PACK_TO_COA: dict[str, str] = {
    "university": "coa.education",
    "school": "coa.education",
    "hospital": "coa.healthcare",
    "clinic": "coa.healthcare",
    "laboratory": "coa.healthcare",
    "bank": "coa.banking",
    "islamic_bank": "coa.islamic_banking",
    "microfinance": "coa.banking",
    "currency_exchange": "coa.forex",
    "accounting_firm": "coa.professional_services",
    "tax_consulting": "coa.tax_services",
    "construction": "coa.construction",
    "manufacturing": "coa.manufacturing",
    "retail": "coa.retail",
    "pos": "coa.retail",
    "government": "coa.government",
    "ngo": "coa.ngo",
    "hotel": "coa.hospitality",
    "restaurant": "coa.hospitality",
    "real_estate": "coa.real_estate",
}

INDUSTRY_COST_CENTERS: dict[str, list[tuple[str, str]]] = {
    "hospital": [("ER", "Emergency"), ("SUR", "Surgery"), ("ADM", "Administration")],
    "university": [("ACD", "Academic"), ("ADM", "Administration"), ("RSH", "Research")],
    "pos": [("STORE", "Store Operations")],
}

_cached_catalog: dict[str, Any] | None = None


def load_template_catalog() -> dict[str, Any]:
    global _cached_catalog
    if _cached_catalog is not None:
        return _cached_catalog
    if not _TEMPLATE_PATH.exists():
        _cached_catalog = {"version": 1, "industry_templates": {}, "country_templates": {}}
        return _cached_catalog
    with _TEMPLATE_PATH.open(encoding="utf-8") as handle:
        _cached_catalog = yaml.safe_load(handle) or {}
    return _cached_catalog


def list_industry_templates() -> list[dict[str, Any]]:
    catalog = load_template_catalog()
    result = []
    for key, spec in (catalog.get("industry_templates") or {}).items():
        result.append(
            {
                "template_key": key,
                "template_type": "industry",
                "name": spec.get("name", key),
                "industries": spec.get("industries", []),
                "description": spec.get("description"),
            }
        )
    return sorted(result, key=lambda x: x["template_key"])


def list_country_templates() -> list[dict[str, Any]]:
    catalog = load_template_catalog()
    result = []
    for key, spec in (catalog.get("country_templates") or {}).items():
        result.append(
            {
                "template_key": key,
                "template_type": "country",
                "name": spec.get("name", key),
                "country_code": spec.get("country_code"),
                "description": spec.get("description"),
            }
        )
    return sorted(result, key=lambda x: x["template_key"])


def get_template_tree(template_key: str, template_type: str = "industry") -> list[dict[str, Any]]:
    catalog = load_template_catalog()
    bucket = (
        catalog.get("industry_templates")
        if template_type == "industry"
        else catalog.get("country_templates")
    ) or {}
    spec = bucket.get(template_key)
    if not spec:
        raise KeyError(f"template_not_found:{template_key}")
    return spec.get("tree", [])


def resolve_account_code(
    node: dict[str, Any],
    *,
    code_overrides: dict[str, str] | None,
    code_prefix: str,
) -> str:
    account_key = node["account_key"]
    if code_overrides and account_key in code_overrides:
        return code_overrides[account_key]
    suggestion = node.get("code_suggestion", "")
    if suggestion:
        return f"{code_prefix}{suggestion}" if code_prefix else suggestion
    return account_key.replace(".", "_").upper()


def materialize_template_tree(
    *,
    tenant_id: str,
    template_key: str,
    template_type: str = "industry",
    code_overrides: dict[str, str] | None = None,
    code_prefix: str = "",
    country_code: str | None = None,
) -> list[ChartOfAccount]:
    """Build tenant account tree from template. Codes are tenant-configurable, never hardcoded in code."""
    tree = get_template_tree(template_key, template_type)
    source = TemplateSource.INDUSTRY if template_type == "industry" else TemplateSource.COUNTRY
    accounts: list[ChartOfAccount] = []
    _materialize_nodes(
        tenant_id=tenant_id,
        nodes=tree,
        parent_id=None,
        parent_path="",
        level=0,
        template_key=template_key,
        template_source=source,
        country_code=country_code,
        code_overrides=code_overrides,
        code_prefix=code_prefix,
        accounts=accounts,
    )
    return accounts


def _materialize_nodes(
    *,
    tenant_id: str,
    nodes: list[dict[str, Any]],
    parent_id: str | None,
    parent_path: str,
    level: int,
    template_key: str,
    template_source: TemplateSource,
    country_code: str | None,
    code_overrides: dict[str, str] | None,
    code_prefix: str,
    accounts: list[ChartOfAccount],
) -> None:
    for node in nodes:
        account_key = node["account_key"]
        path = f"{parent_path}/{account_key}" if parent_path else account_key
        account = ChartOfAccount.create(
            tenant_id=tenant_id,
            code=resolve_account_code(node, code_overrides=code_overrides, code_prefix=code_prefix),
            name=node["name"],
            account_category=AccountCategory(node["category"]),
            account_key=account_key,
            parent_account_id=parent_id,
            level=level,
            tree_path=path,
            account_group=node.get("group"),
            is_posting=node.get("is_posting", True),
            template_source=template_source,
            template_key=template_key,
            country_code=country_code or node.get("country_code"),
        )
        accounts.append(account)
        children = node.get("children") or []
        if children:
            _materialize_nodes(
                tenant_id=tenant_id,
                nodes=children,
                parent_id=str(account.id),
                parent_path=path,
                level=level + 1,
                template_key=template_key,
                template_source=template_source,
                country_code=country_code,
                code_overrides=code_overrides,
                code_prefix=code_prefix,
                accounts=accounts,
            )


def build_accounts(tenant_id: str, template_key: str) -> list[ChartOfAccount]:
    """Provision industry template accounts for a tenant."""
    return materialize_template_tree(
        tenant_id=tenant_id,
        template_key=template_key,
        template_type="industry",
    )
