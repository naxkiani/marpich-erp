"""Chart of Accounts tree operations — unlimited depth, configurable codes."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.chart_of_account import ChartOfAccount


def build_account_tree(accounts: list[ChartOfAccount]) -> list[dict]:
    """Build nested tree from flat account list. Supports unlimited depth."""
    by_id = {str(a.id): {**a.to_dict(), "children": []} for a in accounts}
    roots: list[dict] = []
    for node in by_id.values():
        parent_id = node.get("parent_account_id")
        if parent_id and parent_id in by_id:
            by_id[parent_id]["children"].append(node)
        else:
            roots.append(node)

    def sort_tree(nodes: list[dict]) -> None:
        nodes.sort(key=lambda n: (n.get("level", 0), n.get("code", "")))
        for node in nodes:
            sort_tree(node.get("children", []))

    sort_tree(roots)
    return roots


def validate_parent_assignment(
    account: ChartOfAccount,
    parent: ChartOfAccount | None,
    all_accounts: list[ChartOfAccount],
) -> tuple[bool, str | None]:
    if parent is None:
        return True, None
    if str(account.id) == str(parent.id):
        return False, "self_parent"
    if parent.tenant_id != account.tenant_id:
        return False, "tenant_mismatch"
    if _is_descendant(parent, str(account.id), all_accounts):
        return False, "cycle_detected"
    return True, None


def _is_descendant(
    node: ChartOfAccount, ancestor_id: str, all_accounts: list[ChartOfAccount]
) -> bool:
    by_id = {str(a.id): a for a in all_accounts}
    current: ChartOfAccount | None = node
    while current and current.parent_account_id:
        if current.parent_account_id == ancestor_id:
            return True
        current = by_id.get(current.parent_account_id)
    return False


def flatten_tree(nodes: list[dict]) -> list[dict]:
    result: list[dict] = []
    for node in nodes:
        children = node.get("children", [])
        row = {k: v for k, v in node.items() if k != "children"}
        result.append(row)
        if children:
            result.extend(flatten_tree(children))
    return result
