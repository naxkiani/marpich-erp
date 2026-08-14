"""Quantum P215-M integration / gateway / mesh foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/458-enterprise-quantum-integration.md",
    "docs/architecture/ENTERPRISE_QUANTUM_INTEGRATION.md",
    "docs/architecture/quantum/QUANTUM_INTEGRATION_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_INTEGRATION_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_INTEGRATION_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_INTEGRATION_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_integration.py",
    "backend/contexts/quantum/domain/aggregates/qc_integration_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_integration_acl.py",
    "backend/contexts/quantum/application/qc_integration_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_api_gateway_platform",
    "backend/contexts/quantum_service_mesh_platform",
    "backend/contexts/quantum_hybrid_integration_platform",
    "backend/contexts/quantum_capability_federation_platform",
)
def validate_qc_integration_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_integration_aggregates import (
        QuantumIntegrationPlatformRoot, QuantumApiGatewayRoot, QuantumServiceMeshRoot,
        HybridIntelligenceBridgeRoot, EventIntegrationBackboneRoot, CapabilityFederationRoot,
        IntegrationKnowledgeGraphRoot, IntegrationDigitalTwinRoot,
    )
    from contexts.quantum.domain.services import qc_platform_integration as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-M" and cat["adr"] == 458 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["fabric"] == "meos_quantum_integration_intelligence_fabric"
        and cat["quantum_integration_platform_present_required"] is True
        and cat["quantum_api_gateway_present_required"] is True
        and cat["quantum_service_mesh_present_required"] is True
        and cat["hybrid_intelligence_bridge_present_required"] is True
        and cat["event_integration_backbone_present_required"] is True
        and cat["capability_federation_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["aggregates"]["aggregate_count"] >= 7
        and cat["microservices"]["service_count"] >= 10
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_d"] is True
        and cat["builds_on_p215_e"] is True and cat["builds_on_p215_f"] is True
        and cat["builds_on_p215_h"] is True and cat["builds_on_p215_l"] is True
        and cat["governed_by_p215_k"] is True
        and cat["api_gateway"]["via_platform_api_gateway"] is True
        and cat["api_gateway"]["module_local_gateway_forbidden"] is True
        and cat["event_backbone"]["via_event_fabric"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        QuantumIntegrationPlatformRoot.enable(tenant_id="t1", integration_ref="i1").is_missing() is False,
        QuantumApiGatewayRoot.enable(tenant_id="t1", gateway_ref="g1").is_missing() is False,
        QuantumServiceMeshRoot.enable(tenant_id="t1", mesh_ref="m1").is_missing() is False,
        HybridIntelligenceBridgeRoot.enable(tenant_id="t1", hybrid_ref="h1").is_missing() is False,
        EventIntegrationBackboneRoot.enable(tenant_id="t1", event_ref="e1").is_missing() is False,
        CapabilityFederationRoot.enable(tenant_id="t1", capability_ref="c1").is_missing() is False,
        IntegrationKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="kg1").is_missing() is False,
        IntegrationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_integration_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_d", "via_p215_e", "via_p215_f", "via_p215_g", "via_p215_h",
        "via_p215_i", "via_p215_j", "via_p215_k", "via_p215_l", "via_p214_z",
        "via_platform_api_gateway", "via_integration_platform", "via_event_fabric",
        "module_local_gateway_forbidden", "module_local_broker_forbidden",
        "module_local_quantum_integration_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/integration")', "/integration/api-gateway", "/integration/service-mesh",
        "/integration/hybrid", "/integration/connectors", "/integration/events",
        "/integration/capabilities", "/integration/governance", "/integration/intelligence",
        "/integration/knowledge-graph", "/integration/digital-twin", "/integration/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_INTEGRATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Integration Platform is missing",
        "Never Quantum API Gateway is missing",
        "Never Quantum Service Mesh is missing",
        "Never Hybrid Intelligence Bridge is missing",
        "Never Event Integration Backbone is missing",
        "Never Capability Federation is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "MEOS Quantum Integration Platform SHALL provide",
        "P215-A", "P215-D", "P215-E", "P215-F", "P215-H", "P215-K", "P215-L",
        "Platform API Gateway", "Integration Platform", "Event Fabric",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-M", "adr": 458, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
