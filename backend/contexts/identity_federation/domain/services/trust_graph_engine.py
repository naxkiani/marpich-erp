"""Enterprise Trust Graph — nodes, edges, queries, lifecycle (federation projection)."""
from __future__ import annotations

from enum import StrEnum


class TrustNodeType(StrEnum):
    IDENTITY = "identity"
    ORGANIZATION = "organization"
    TENANT = "tenant"
    APPLICATION = "application"
    API = "api"
    DEVICE = "device"
    BROWSER = "browser"
    SESSION = "session"
    CERTIFICATE = "certificate"
    TOKEN = "token"
    ROLE = "role"
    PERMISSION = "permission"
    DEPARTMENT = "department"
    PARTNER = "partner"
    AI_AGENT = "ai_agent"
    SERVICE_ACCOUNT = "service_account"


class TrustEdgeType(StrEnum):
    TRUST = "trust"
    DELEGATION = "delegation"
    FEDERATION = "federation"
    OWNERSHIP = "ownership"
    MEMBERSHIP = "membership"
    AUTHORIZATION = "authorization"
    PROVISIONING = "provisioning"
    SYNCHRONIZATION = "synchronization"
    INHERITANCE = "inheritance"


def empty_graph(tenant_id: str) -> dict:
    return {"tenant_id": tenant_id, "nodes": {}, "edges": [], "version": 1}


def upsert_node(graph: dict, *, node_id: str, node_type: str, attributes: dict | None = None) -> dict:
    graph["nodes"][node_id] = {
        "node_id": node_id,
        "node_type": node_type,
        "attributes": attributes or {},
        "status": "active",
    }
    return graph["nodes"][node_id]


def add_edge(
    graph: dict,
    *,
    edge_id: str,
    from_id: str,
    to_id: str,
    relation: str,
    weight: float = 1.0,
    metadata: dict | None = None,
) -> dict:
    edge = {
        "edge_id": edge_id,
        "from": from_id,
        "to": to_id,
        "relation": relation,
        "weight": weight,
        "metadata": metadata or {},
        "status": "active",
    }
    graph["edges"].append(edge)
    return edge


def query_neighbors(graph: dict, *, node_id: str, relation: str | None = None, depth: int = 1) -> dict:
    depth = max(1, min(depth, 5))
    visited = {node_id}
    frontier = {node_id}
    found_edges: list[dict] = []
    for _ in range(depth):
        next_frontier: set[str] = set()
        for edge in graph.get("edges", []):
            if edge.get("status") != "active":
                continue
            if relation and edge.get("relation") != relation:
                continue
            if edge["from"] in frontier:
                found_edges.append(edge)
                if edge["to"] not in visited:
                    visited.add(edge["to"])
                    next_frontier.add(edge["to"])
            elif edge["to"] in frontier:
                found_edges.append(edge)
                if edge["from"] not in visited:
                    visited.add(edge["from"])
                    next_frontier.add(edge["from"])
        frontier = next_frontier
        if not frontier:
            break
    nodes = {nid: graph["nodes"][nid] for nid in visited if nid in graph.get("nodes", {})}
    return {"root": node_id, "depth": depth, "nodes": list(nodes.values()), "edges": found_edges}


def find_path(graph: dict, *, source: str, target: str, max_depth: int = 6) -> dict:
    """BFS shortest trust path."""
    if source == target:
        return {"found": True, "path": [source], "hops": 0}
    adj: dict[str, list[str]] = {}
    for e in graph.get("edges", []):
        if e.get("status") != "active":
            continue
        adj.setdefault(e["from"], []).append(e["to"])
        adj.setdefault(e["to"], []).append(e["from"])
    queue = [(source, [source])]
    seen = {source}
    while queue:
        node, path = queue.pop(0)
        if len(path) > max_depth:
            continue
        for nxt in adj.get(node, []):
            if nxt in seen:
                continue
            new_path = path + [nxt]
            if nxt == target:
                return {"found": True, "path": new_path, "hops": len(new_path) - 1}
            seen.add(nxt)
            queue.append((nxt, new_path))
    return {"found": False, "path": [], "hops": -1}


def propagate_trust(graph: dict, *, source: str, base_score: int = 80, decay: float = 0.85) -> dict:
    """Propagate trust scores along edges with decay."""
    scores = {source: float(base_score)}
    frontier = [source]
    while frontier:
        current = frontier.pop(0)
        current_score = scores[current]
        for edge in graph.get("edges", []):
            if edge.get("from") != current or edge.get("status") != "active":
                continue
            nxt = edge["to"]
            candidate = current_score * decay * float(edge.get("weight", 1.0))
            if candidate > scores.get(nxt, -1):
                scores[nxt] = candidate
                frontier.append(nxt)
    return {
        "source": source,
        "scores": {k: int(v) for k, v in scores.items()},
        "nodes_reached": len(scores),
    }


def graph_lifecycle_transition(status: str, event: str) -> str | None:
    transitions = {
        ("pending", "activate"): "active",
        ("active", "suspend"): "suspended",
        ("suspended", "resume"): "active",
        ("active", "revoke"): "revoked",
        ("suspended", "revoke"): "revoked",
    }
    return transitions.get((status, event))


def catalog() -> dict:
    return {
        "node_types": [t.value for t in TrustNodeType],
        "edge_types": [t.value for t in TrustEdgeType],
        "queries": ["neighbors", "path", "propagate", "subgraph"],
    }
