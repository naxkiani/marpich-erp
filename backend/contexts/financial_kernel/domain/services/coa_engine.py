"""Enterprise Chart of Accounts engine — configurable account trees."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.account_types import AccountCategory
from contexts.financial_kernel.domain.aggregates.chart_of_account import ChartOfAccount

CATEGORY_ROOTS: list[dict] = [
    {"category": AccountCategory.ASSET.value, "name": "Assets", "account_key": "assets"},
    {"category": AccountCategory.LIABILITY.value, "name": "Liabilities", "account_key": "liabilities"},
    {"category": AccountCategory.EQUITY.value, "name": "Equity", "account_key": "equity"},
    {"category": AccountCategory.REVENUE.value, "name": "Revenue", "account_key": "revenue"},
    {"category": AccountCategory.EXPENSE.value, "name": "Expenses", "account_key": "expenses"},
    {"category": AccountCategory.OFF_BALANCE.value, "name": "Off Balance Sheet", "account_key": "off_balance"},
    {"category": AccountCategory.STATISTICAL.value, "name": "Statistical Accounts", "account_key": "statistical"},
]


def validate_account_fields(
    *,
    code: str,
    name: str,
    account_category: str,
    is_posting: bool,
    parent: ChartOfAccount | None,
) -> tuple[bool, str | None]:
    if not code.strip():
        return False, "missing_code"
    if not name.strip():
        return False, "missing_name"
    try:
        AccountCategory(account_category)
    except ValueError:
        return False, "invalid_category"
    if parent and not parent.is_posting and is_posting is False and parent.level == 0:
        pass  # summary under summary is valid
    if parent and parent.account_category.value != account_category:
        return False, "category_mismatch_with_parent"
    return True, None


def enrich_tree_metadata(node: dict) -> dict:
    """Attach enterprise metadata defaults for tree display."""
    category = node.get("account_category") or node.get("category")
    return {
        **node,
        "category_label": category,
        "is_summary": not node.get("is_posting", True),
        "has_children": bool(node.get("children")),
        "depth": node.get("level", 0),
    }


def build_enriched_tree(accounts: list[ChartOfAccount]) -> list[dict]:
    from contexts.financial_kernel.domain.services.coa_tree_service import build_account_tree

    tree = build_account_tree(accounts)

    def walk(nodes: list[dict]) -> list[dict]:
        result = []
        for node in nodes:
            children = node.get("children", [])
            enriched = enrich_tree_metadata(node)
            enriched["children"] = walk(children)
            result.append(enriched)
        return result

    return walk(tree)


def count_tree_depth(nodes: list[dict], depth: int = 0) -> int:
    if not nodes:
        return depth
    max_child = depth
    for node in nodes:
        children = node.get("children", [])
        if children:
            max_child = max(max_child, count_tree_depth(children, depth + 1))
        else:
            max_child = max(max_child, depth)
    return max_child


def find_node_by_key(nodes: list[dict], account_key: str) -> dict | None:
    for node in nodes:
        if node.get("account_key") == account_key:
            return node
        found = find_node_by_key(node.get("children", []), account_key)
        if found:
            return found
    return None


def template_node_metadata(node: dict) -> dict:
    """Extract enterprise account metadata from template YAML node."""
    return {
        "currency": node.get("currency"),
        "is_control_account": node.get("is_control_account", False),
        "reconciliation_required": node.get("reconciliation_required", False),
        "tax_code": node.get("tax_code") or node.get("tax_mapping"),
        "budget_code": node.get("budget_code") or node.get("budget_mapping"),
        "status": node.get("status", "active"),
        "effective_date": node.get("effective_date"),
    }
