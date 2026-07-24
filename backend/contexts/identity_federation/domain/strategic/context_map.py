"""Context map relationships — cycle detection for strategic DDD gates."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ContextRelation:
    relation_id: str
    relation_type: str
    source: str
    target: str


# Directed edges used only for cycle analysis of *model coupling* (not runtime calls).
# Separate Ways / OHS publish do not create coupling edges.
COUPLING_EDGES: tuple[ContextRelation, ...] = (
    ContextRelation("REL_FED_ID_CS", "customer_supplier", "identity_federation", "identity"),
    ContextRelation("REL_FED_INT_ACL", "acl", "identity_federation", "integration"),
    ContextRelation("REL_FED_ADA_ACL", "acl", "identity_federation", "adaptive_authentication"),
    ContextRelation("REL_FED_RISK_ACL", "acl", "identity_federation", "identity_risk"),
    ContextRelation("REL_AUTHZ_POL_CS", "customer_supplier", "authorization", "policy"),
)


def has_circular_dependency(edges: tuple[ContextRelation, ...] = COUPLING_EDGES) -> bool:
    graph: dict[str, list[str]] = {}
    for e in edges:
        graph.setdefault(e.source, []).append(e.target)
        graph.setdefault(e.target, [])

    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for nxt in graph.get(node, []):
            if dfs(nxt):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(dfs(n) for n in graph)


SEPARATE_WAYS = frozenset({("identity_federation", "authorization"), ("authorization", "identity_federation")})
