"""Enterprise account hierarchy engine — trees, versioning, validation, visual."""
from __future__ import annotations

import re
from typing import Any

from contexts.financial_kernel.domain.aggregates.chart_of_account import ChartOfAccount
from contexts.financial_kernel.domain.services.coa_engine import build_enriched_tree
from contexts.financial_kernel.domain.services.coa_tree_service import (
    build_account_tree,
    flatten_tree,
    validate_parent_assignment,
)

MAX_RECOMMENDED_DEPTH = 12


def filter_accounts_for_tree(
    accounts: list[ChartOfAccount],
    tree_id: str | None,
    *,
    include_unassigned: bool = True,
) -> list[ChartOfAccount]:
    if tree_id is None:
        return list(accounts)
    result: list[ChartOfAccount] = []
    for account in accounts:
        account_tree_id = getattr(account, "tree_id", None)
        if account_tree_id == tree_id:
            result.append(account)
        elif include_unassigned and account_tree_id is None:
            result.append(account)
    return result


def compute_tree_stats(accounts: list[ChartOfAccount]) -> dict[str, int]:
    if not accounts:
        return {"account_count": 0, "max_depth": 0}
    return {
        "account_count": len(accounts),
        "max_depth": max(a.level for a in accounts) + 1 if accounts else 0,
    }


def detect_duplicates(accounts: list[ChartOfAccount]) -> list[dict]:
    issues: list[dict] = []
    codes: dict[str, list[str]] = {}
    keys: dict[str, list[str]] = {}
    for account in accounts:
        aid = str(account.id)
        codes.setdefault(account.code, []).append(aid)
        if account.account_key:
            keys.setdefault(account.account_key, []).append(aid)
    for code, ids in codes.items():
        if len(ids) > 1:
            issues.append(
                {"issue_type": "duplicate_code", "value": code, "account_ids": ids}
            )
    for key, ids in keys.items():
        if len(ids) > 1:
            issues.append(
                {"issue_type": "duplicate_key", "value": key, "account_ids": ids}
            )
    return issues


def validate_tree_integrity(accounts: list[ChartOfAccount]) -> dict:
    issues: list[dict] = []
    by_id = {str(a.id): a for a in accounts}
    roots = [a for a in accounts if not a.parent_account_id]

    for account in accounts:
        parent_id = account.parent_account_id
        if parent_id and parent_id not in by_id:
            issues.append(
                {
                    "issue_type": "orphan_account",
                    "account_id": str(account.id),
                    "code": account.code,
                    "message": "parent_not_found",
                    "parent_account_id": parent_id,
                }
            )
        if parent_id:
            parent = by_id.get(parent_id)
            if parent:
                ok, reason = validate_parent_assignment(account, parent, accounts)
                if not ok:
                    issues.append(
                        {
                            "issue_type": "parent_child_integrity",
                            "account_id": str(account.id),
                            "code": account.code,
                            "message": reason,
                        }
                    )

    if not accounts:
        return {"valid": True, "issues": [], "root_count": 0, "max_depth": 0}

    max_depth = max(a.level for a in accounts) + 1
    if max_depth > MAX_RECOMMENDED_DEPTH:
        issues.append(
            {
                "issue_type": "deep_nesting",
                "message": "exceeds_recommended_depth",
                "max_depth": max_depth,
                "recommended_max": MAX_RECOMMENDED_DEPTH,
            }
        )

    for dup in detect_duplicates(accounts):
        issues.append({**dup, "message": "duplicate_detected"})

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "root_count": len(roots),
        "max_depth": max_depth,
    }


def search_tree_accounts(
    accounts: list[ChartOfAccount],
    *,
    query: str = "",
    account_category: str | None = None,
    account_type: str | None = None,
    is_posting: bool | None = None,
    level: int | None = None,
    parent_account_id: str | None = None,
) -> list[dict]:
    q = query.strip().lower()
    results: list[dict] = []
    for account in accounts:
        if account_category and account.account_category.value != account_category:
            continue
        if account_type and account.account_type != account_type:
            continue
        if is_posting is not None and account.is_posting != is_posting:
            continue
        if level is not None and account.level != level:
            continue
        if parent_account_id is not None and account.parent_account_id != parent_account_id:
            continue
        if q:
            haystack = " ".join(
                filter(
                    None,
                    [
                        account.code,
                        account.name,
                        account.account_key or "",
                        account.tree_path,
                        account.account_group or "",
                    ],
                )
            ).lower()
            if q not in haystack:
                continue
        results.append(account.to_dict())
    results.sort(key=lambda r: (r.get("level", 0), r.get("code", "")))
    return results


def compute_move_updates(
    *,
    account: ChartOfAccount,
    new_parent: ChartOfAccount | None,
    all_accounts: list[ChartOfAccount],
    position: int | None = None,
) -> tuple[bool, str, list[dict]]:
    if new_parent:
        ok, reason = validate_parent_assignment(account, new_parent, all_accounts)
        if not ok:
            return False, reason or "invalid_parent", []

    new_level = 0 if new_parent is None else new_parent.level + 1
    segment = account.account_key or account.code
    new_path = segment if new_parent is None else f"{new_parent.tree_path}/{segment}"
    new_parent_id = str(new_parent.id) if new_parent else None

    update_map: dict[str, dict] = {
        str(account.id): {
            "account_id": str(account.id),
            "parent_account_id": new_parent_id,
            "level": new_level,
            "tree_path": new_path,
            "display_order": position if position is not None else account.display_order,
        }
    }

    queue = [str(account.id)]
    while queue:
        parent_id = queue.pop(0)
        parent_entry = update_map[parent_id]
        for child in direct_children_by_id(parent_id, all_accounts):
            child_segment = child.account_key or child.code
            child_path = f"{parent_entry['tree_path']}/{child_segment}"
            child_level = parent_entry["level"] + 1
            if str(child.id) not in update_map:
                update_map[str(child.id)] = {
                    "account_id": str(child.id),
                    "parent_account_id": child.parent_account_id,
                    "level": child_level,
                    "tree_path": child_path,
                    "display_order": child.display_order,
                }
                queue.append(str(child.id))
            else:
                update_map[str(child.id)]["level"] = child_level
                update_map[str(child.id)]["tree_path"] = child_path

    return True, "", list(update_map.values())


def direct_children_by_id(parent_id: str, accounts: list[ChartOfAccount]) -> list[ChartOfAccount]:
    return [a for a in accounts if a.parent_account_id == parent_id]


def apply_account_updates(account: ChartOfAccount, update: dict) -> None:
    account.parent_account_id = update.get("parent_account_id")
    account.level = update.get("level", account.level)
    account.tree_path = update.get("tree_path", account.tree_path)
    if "display_order" in update:
        account.display_order = update["display_order"]


def build_version_snapshot(accounts: list[ChartOfAccount]) -> list[dict]:
    tree = build_enriched_tree(accounts)
    flat = flatten_tree(tree)
    return [
        {
            "id": row["id"],
            "code": row["code"],
            "name": row["name"],
            "account_key": row.get("account_key"),
            "parent_account_id": row.get("parent_account_id"),
            "level": row.get("level", 0),
            "tree_path": row.get("tree_path", ""),
            "account_category": row.get("account_category"),
            "account_type": row.get("account_type"),
            "is_posting": row.get("is_posting", True),
            "display_order": row.get("display_order", 0),
        }
        for row in flat
    ]


def validate_bulk_import_rows(
    rows: list[dict],
    existing_accounts: list[ChartOfAccount],
) -> dict:
    issues: list[dict] = []
    seen_codes: set[str] = set()
    seen_keys: set[str] = set()
    existing_codes = {a.code for a in existing_accounts}
    existing_keys = {a.account_key for a in existing_accounts if a.account_key}

    for index, row in enumerate(rows):
        code = str(row.get("code", "")).strip()
        name = str(row.get("name", "")).strip()
        if not code:
            issues.append({"row": index, "field": "code", "message": "required"})
        if not name:
            issues.append({"row": index, "field": "name", "message": "required"})
        if code in seen_codes:
            issues.append({"row": index, "field": "code", "message": "duplicate_in_batch"})
        if code in existing_codes:
            issues.append({"row": index, "field": "code", "message": "already_exists"})
        seen_codes.add(code)

        account_key = row.get("account_key")
        if account_key:
            key = str(account_key).strip()
            if key in seen_keys:
                issues.append({"row": index, "field": "account_key", "message": "duplicate_in_batch"})
            if key in existing_keys:
                issues.append({"row": index, "field": "account_key", "message": "already_exists"})
            seen_keys.add(key)

        parent_code = row.get("parent_code")
        parent_id = row.get("parent_account_id")
        if parent_code and parent_id:
            issues.append({"row": index, "message": "parent_code_and_parent_id_conflict"})

    parent_codes_in_batch = {str(r.get("code", "")).strip() for r in rows if r.get("code")}
    for index, row in enumerate(rows):
        parent_code = row.get("parent_code")
        if parent_code:
            pc = str(parent_code).strip()
            if pc not in existing_codes and pc not in parent_codes_in_batch:
                issues.append({"row": index, "field": "parent_code", "message": "parent_not_found"})

    return {"valid": len(issues) == 0, "issues": issues, "row_count": len(rows)}


def export_bulk_rows(accounts: list[ChartOfAccount]) -> list[dict]:
    by_id = {str(a.id): a for a in accounts}
    rows: list[dict] = []
    for account in sorted(accounts, key=lambda a: (a.level, a.display_order, a.code)):
        parent_code = None
        if account.parent_account_id:
            parent = by_id.get(account.parent_account_id)
            parent_code = parent.code if parent else None
        rows.append(
            {
                "code": account.code,
                "name": account.name,
                "account_key": account.account_key,
                "parent_code": parent_code,
                "parent_account_id": account.parent_account_id,
                "account_category": account.account_category.value,
                "account_type": account.account_type,
                "is_posting": account.is_posting,
                "level": account.level,
                "tree_path": account.tree_path,
                "display_order": account.display_order,
            }
        )
    return rows


def generate_ai_tree_optimization(
    accounts: list[ChartOfAccount],
    *,
    tree_name: str = "",
) -> dict:
    integrity = validate_tree_integrity(accounts)
    duplicates = detect_duplicates(accounts)
    suggestions: list[dict] = []
    score = 100

    if duplicates:
        score -= min(30, len(duplicates) * 10)
        suggestions.append(
            {
                "priority": "high",
                "category": "duplicates",
                "message": "Resolve duplicate account codes or keys before go-live.",
                "count": len(duplicates),
            }
        )

    orphans = [i for i in integrity["issues"] if i.get("message") == "parent_not_found"]
    if orphans:
        score -= min(25, len(orphans) * 5)
        suggestions.append(
            {
                "priority": "high",
                "category": "orphans",
                "message": "Re-parent or remove orphaned accounts.",
                "count": len(orphans),
            }
        )

    deep = integrity.get("max_depth", 0)
    if deep > MAX_RECOMMENDED_DEPTH:
        score -= 15
        suggestions.append(
            {
                "priority": "medium",
                "category": "depth",
                "message": f"Tree depth ({deep}) exceeds recommended {MAX_RECOMMENDED_DEPTH}; consider flattening summary groups.",
            }
        )

    posting_parents = [
        a for a in accounts if a.is_posting and await_children(a, accounts)
    ]
    if posting_parents:
        score -= min(20, len(posting_parents) * 4)
        suggestions.append(
            {
                "priority": "medium",
                "category": "posting_parents",
                "message": "Posting accounts with children may confuse trial balance rollups; use summary parents.",
                "account_codes": [a.code for a in posting_parents[:10]],
            }
        )

    single_child_parents = [
        a for a in accounts if len(direct_children(a, accounts)) == 1
    ]
    if len(single_child_parents) > 3:
        score -= 10
        suggestions.append(
            {
                "priority": "low",
                "category": "structure",
                "message": "Several nodes have only one child; merge redundant levels where possible.",
                "count": len(single_child_parents),
            }
        )

    empty_summaries = [
        a
        for a in accounts
        if not a.is_posting and not direct_children(a, accounts)
    ]
    if empty_summaries:
        score -= 5
        suggestions.append(
            {
                "priority": "low",
                "category": "empty_groups",
                "message": "Summary accounts without children can be removed or populated.",
                "count": len(empty_summaries),
            }
        )

    score = max(0, score)
    recommendation = "optimal" if score >= 85 else "review" if score >= 60 else "restructure"
    return {
        "tree_name": tree_name,
        "optimization_score": score,
        "recommendation": recommendation,
        "integrity": integrity,
        "duplicate_count": len(duplicates),
        "suggestions": suggestions,
    }


def direct_children(account: ChartOfAccount, accounts: list[ChartOfAccount]) -> list[ChartOfAccount]:
    aid = str(account.id)
    return [a for a in accounts if a.parent_account_id == aid]


def await_children(account: ChartOfAccount, accounts: list[ChartOfAccount]) -> bool:
    return bool(direct_children(account, accounts))


def _safe_mermaid_id(raw: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "_", raw)
    return cleaned or "node"


def generate_visual_account_tree(roots: list[dict]) -> dict[str, Any]:
    mermaid_lines = ["flowchart TD"]
    visual_nodes: list[dict] = []
    visual_edges: list[dict] = []
    seen: set[str] = set()

    def walk(node: dict, parent_visual_id: str | None = None, depth: int = 0) -> None:
        node_id = _safe_mermaid_id(node["id"])
        if node_id in seen:
            node_id = f"{node_id}_{len(seen)}"
        seen.add(node_id)
        label = f"{node.get('code', '')} {node.get('name', '')}".strip()
        category = node.get("account_category", "")
        mermaid_lines.append(f'    {node_id}["{label}"]')
        visual_nodes.append(
            {
                "id": node["id"],
                "mermaid_id": node_id,
                "label": label,
                "code": node.get("code"),
                "name": node.get("name"),
                "level": node.get("level", depth),
                "account_category": category,
                "is_posting": node.get("is_posting", True),
                "is_summary": node.get("is_summary", not node.get("is_posting", True)),
            }
        )
        if parent_visual_id:
            mermaid_lines.append(f"    {parent_visual_id} --> {node_id}")
            visual_edges.append(
                {"from": parent_visual_id, "to": node_id, "type": "parent_child"}
            )
        for child in sorted(
            node.get("children", []),
            key=lambda c: (c.get("display_order", 0), c.get("code", "")),
        ):
            walk(child, node_id, depth + 1)

    for root in roots:
        walk(root)

    max_depth = max((n["level"] for n in visual_nodes), default=0) + 1
    return {
        "format": "hierarchy",
        "layout": "top_down",
        "max_depth": max_depth,
        "node_count": len(visual_nodes),
        "mermaid": "\n".join(mermaid_lines),
        "visual": {
            "nodes": visual_nodes,
            "edges": visual_edges,
            "layout": {"direction": "TB", "level_separation": 80, "node_separation": 40},
        },
    }


def build_hierarchy_tree(accounts: list[ChartOfAccount]) -> list[dict]:
    return build_enriched_tree(accounts)


def resolve_parent_from_import_row(
    row: dict,
    *,
    code_to_id: dict[str, str],
    batch_code_to_id: dict[str, str],
) -> str | None:
    if row.get("parent_account_id"):
        return row["parent_account_id"]
    parent_code = row.get("parent_code")
    if not parent_code:
        return None
    pc = str(parent_code).strip()
    return batch_code_to_id.get(pc) or code_to_id.get(pc)
