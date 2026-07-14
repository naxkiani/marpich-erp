"""Enterprise Identity Fabric Mesh — controller, registry, discovery, routing."""
from __future__ import annotations

from enum import StrEnum


class MeshNodeType(StrEnum):
    INTERNAL_IDP = "internal_idp"
    EXTERNAL_IDP = "external_idp"
    GOVERNMENT = "government"
    BANKING = "banking"
    UNIVERSITY = "university"
    HEALTHCARE = "healthcare"
    ERP = "erp"
    HR = "hr"
    CRM = "crm"
    SAAS = "saas"
    MOBILE = "mobile"
    DESKTOP = "desktop"
    AI_AGENT = "ai_agent"
    API_CONSUMER = "api_consumer"


MESH_NODE_CATALOG = [
    {"type": t.value, "category": "identity_source" if "idp" in t.value or t.value in (
        "government", "banking", "university", "healthcare"
    ) else "consumer"}
    for t in MeshNodeType
]


def build_mesh_topology(*, providers: list[dict], partners: list[dict], tenants: list[dict] | None = None) -> dict:
    nodes: list[dict] = []
    edges: list[dict] = []
    for p in providers:
        protocol = p.get("protocol", "oidc")
        node_type = _protocol_to_node_type(protocol, p.get("config") or {})
        node_id = f"idp:{p.get('provider_ref')}"
        nodes.append({
            "node_id": node_id,
            "node_type": node_type,
            "label": p.get("name"),
            "protocol": protocol,
            "enabled": p.get("enabled", True),
            "status": "healthy" if p.get("enabled", True) else "disabled",
        })
        edges.append({
            "edge_id": f"fed:{p.get('provider_ref')}",
            "from": "mesh:controller",
            "to": node_id,
            "relation": "federation",
            "protocol": protocol,
        })
    for partner in partners:
        node_id = f"partner:{partner.get('partner_ref')}"
        nodes.append({
            "node_id": node_id,
            "node_type": "partner",
            "label": partner.get("name"),
            "trust_level": partner.get("trust_level", "medium"),
            "status": "active",
        })
        edges.append({
            "edge_id": f"trust:{partner.get('partner_ref')}",
            "from": "mesh:controller",
            "to": node_id,
            "relation": "trust",
        })
    for tenant in tenants or []:
        node_id = f"tenant:{tenant.get('federation_ref', tenant.get('tenant_id'))}"
        nodes.append({
            "node_id": node_id,
            "node_type": "tenant",
            "label": tenant.get("federation_mode", "dedicated"),
            "status": "active",
        })
    nodes.insert(0, {
        "node_id": "mesh:controller",
        "node_type": "controller",
        "label": "Identity Mesh Controller",
        "status": "healthy",
    })
    return {
        "controller": "identity_mesh_controller",
        "gateway": "identity_mesh_gateway",
        "registry": {"node_count": len(nodes), "edge_count": len(edges)},
        "nodes": nodes,
        "edges": edges,
        "capabilities": [
            "discovery", "synchronization", "routing", "monitoring", "zero_trust",
        ],
        "catalog": MESH_NODE_CATALOG,
    }


def _protocol_to_node_type(protocol: str, config: dict) -> str:
    industry = (config.get("industry") or config.get("sector") or "").lower()
    mapping = {
        "government": MeshNodeType.GOVERNMENT.value,
        "banking": MeshNodeType.BANKING.value,
        "bank": MeshNodeType.BANKING.value,
        "university": MeshNodeType.UNIVERSITY.value,
        "healthcare": MeshNodeType.HEALTHCARE.value,
        "hospital": MeshNodeType.HEALTHCARE.value,
    }
    if industry in mapping:
        return mapping[industry]
    if protocol in ("ldap", "ldaps", "ad"):
        return MeshNodeType.INTERNAL_IDP.value
    return MeshNodeType.EXTERNAL_IDP.value


def discover_mesh_route(*, email: str | None, node_hint: str | None, topology: dict) -> dict:
    """Route authentication through the mesh based on email domain or hint."""
    nodes = [n for n in topology.get("nodes", []) if n.get("node_type") != "controller"]
    if node_hint:
        for n in nodes:
            if n.get("node_id") == node_hint or n.get("label") == node_hint:
                return {"routed": True, "target": n, "method": "hint"}
    if email and "@" in email:
        domain = email.split("@", 1)[1].lower()
        for n in nodes:
            # Domain matching via edge metadata is config-driven in provider config
            if domain in str(n.get("label", "")).lower():
                return {"routed": True, "target": n, "method": "domain_match"}
    enabled = [
        n for n in nodes
        if n.get("enabled", True)
        and (
            str(n.get("node_type", "")).endswith("idp")
            or n.get("node_type") in (
                MeshNodeType.EXTERNAL_IDP.value,
                MeshNodeType.INTERNAL_IDP.value,
                MeshNodeType.GOVERNMENT.value,
                MeshNodeType.BANKING.value,
                MeshNodeType.UNIVERSITY.value,
                MeshNodeType.HEALTHCARE.value,
            )
        )
    ]
    if enabled:
        return {"routed": True, "target": enabled[0], "method": "default_enabled"}
    return {"routed": False, "target": None, "method": "none"}


def mesh_health(*, topology: dict) -> dict:
    nodes = topology.get("nodes", [])
    healthy = sum(1 for n in nodes if n.get("status") in ("healthy", "active"))
    return {
        "status": "healthy" if healthy == len(nodes) else "degraded",
        "total_nodes": len(nodes),
        "healthy_nodes": healthy,
        "edges": len(topology.get("edges", [])),
        "monitoring": "identity_mesh_monitoring",
    }


def synchronize_mesh_node(*, node_id: str, direction: str = "inbound") -> dict:
    return {
        "synchronized": True,
        "node_id": node_id,
        "direction": direction,
        "engine": "identity_mesh_synchronization",
    }
