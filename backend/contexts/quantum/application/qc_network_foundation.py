"""Quantum P215-J network/internet foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/456-enterprise-quantum-network.md",
    "docs/architecture/ENTERPRISE_QUANTUM_NETWORK.md",
    "docs/architecture/quantum/QUANTUM_NETWORK_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_NETWORK_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_NETWORK_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_NETWORK_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_network.py",
    "backend/contexts/quantum/domain/aggregates/qc_network_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_network_acl.py",
    "backend/contexts/quantum/application/qc_network_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_network_platform",
    "backend/contexts/quantum_internet_platform",
    "backend/contexts/quantum_communication_platform",
    "backend/contexts/quantum_entanglement_platform",
)
def validate_qc_network_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_network_aggregates import (
        QuantumInternetPlatformRoot, NetworkFabricRoot, CommunicationPlatformRoot,
        NodeFederationRoot, RoutingIntelligenceRoot, NetworkControlPlaneRoot,
        NetworkSecurityIntegrationRoot, NetworkTwinRoot, NetworkKnowledgeGraphRoot,
    )
    from contexts.quantum.domain.services import qc_platform_network as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-J" and cat["adr"] == 456 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["quantum_internet_platform_present_required"] is True
        and cat["quantum_network_fabric_present_required"] is True
        and cat["quantum_communication_platform_present_required"] is True
        and cat["quantum_node_federation_present_required"] is True
        and cat["quantum_routing_intelligence_present_required"] is True
        and cat["quantum_network_control_plane_present_required"] is True
        and cat["quantum_security_integration_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["aggregates"]["aggregate_count"] >= 8
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_d"] is True
        and cat["builds_on_p215_h"] is True and cat["builds_on_p215_i"] is True
        and cat["governed_by_p215_k"] is True
    )
    checks = [
        QuantumInternetPlatformRoot.enable(tenant_id="t1", internet_ref="i1").is_missing() is False,
        NetworkFabricRoot.enable(tenant_id="t1", fabric_ref="f1").is_missing() is False,
        CommunicationPlatformRoot.enable(tenant_id="t1", communication_ref="c1").is_missing() is False,
        NodeFederationRoot.enable(tenant_id="t1", federation_ref="n1").is_missing() is False,
        RoutingIntelligenceRoot.enable(tenant_id="t1", routing_ref="r1").is_missing() is False,
        NetworkControlPlaneRoot.enable(tenant_id="t1", control_ref="cp1").is_missing() is False,
        NetworkSecurityIntegrationRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        NetworkTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        NetworkKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_network_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_d", "via_p215_f", "via_p215_h", "via_p215_i", "via_p215_k",
        "via_p214_z", "via_p214_j", "module_local_quantum_network_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/network")', "/network/nodes", "/network/communication",
        "/network/entanglement", "/network/routing", "/network/control-plane",
        "/network/security", "/network/operations", "/network/knowledge-graph",
        "/network/digital-twin", "/network/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_NETWORK.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Internet Platform is missing",
        "Never Quantum Network Fabric is missing",
        "Never Quantum Communication Platform is missing",
        "Never Quantum Node Federation is missing",
        "Never Quantum Routing Intelligence is missing",
        "Never Quantum Network Control Plane is missing",
        "Never Quantum Security Integration is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "P215-A", "P215-D", "P215-H", "P215-I",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-J", "adr": 456, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
