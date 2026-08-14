"""Quantum P215-T OS / control plane / intelligence core foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/465-enterprise-quantum-os.md",
    "docs/architecture/ENTERPRISE_QUANTUM_OS.md",
    "docs/architecture/quantum/QUANTUM_OS_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_OS_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_OS_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_OS_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_os.py",
    "backend/contexts/quantum/domain/aggregates/qc_os_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_os_acl.py",
    "backend/contexts/quantum/application/qc_os_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_os_platform",
    "backend/contexts/quantum_control_plane_platform",
    "backend/contexts/quantum_intelligence_core_platform",
    "backend/contexts/quantum_orchestration_platform",
    "backend/contexts/quantum_autonomous_governance_platform",
)
def validate_qc_os_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_os_aggregates import (
        QuantumOperatingSystemRoot, QuantumControlPlaneRoot, AutonomousGovernanceRoot,
        QuantumIntelligenceCoreRoot, ResourceOrchestrationRoot, PolicyEngineBindingRoot,
        AgentManagementRoot, OsKnowledgeGraphRoot, OsDigitalTwinRoot,
    )
    from contexts.quantum.domain.services import qc_platform_os as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-T" and cat["adr"] == 465 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["fabric"] == "meos_quantum_intelligence_operating_fabric"
        and cat["trust_gate"] == "P215-K" and cat["security_gate"] == "P215-H"
        and cat["quantum_operating_system_present_required"] is True
        and cat["quantum_control_plane_present_required"] is True
        and cat["autonomous_governance_present_required"] is True
        and cat["quantum_intelligence_core_present_required"] is True
        and cat["resource_orchestration_present_required"] is True
        and cat["policy_engine_present_required"] is True
        and cat["agent_management_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["aggregates"]["aggregate_count"] >= 7
        and cat["microservices"]["service_count"] >= 9
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_d"] is True
        and cat["builds_on_p215_r"] is True and cat["builds_on_p215_s"] is True
        and cat["via_policy_engine"] is True and cat["via_p214_z"] is True
        and cat["never_replace_core_platform"] is True
        and cat["never_replace_p215_k"] is True and cat["never_replace_p215_h"] is True
        and cat["operating_system"]["never_replace_core_platform"] is True
        and cat["policy_execution"]["module_local_pdp_forbidden"] is True
        and cat["intelligence_core"]["module_local_llm_forbidden"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        QuantumOperatingSystemRoot.enable(tenant_id="t1", os_ref="os1").is_missing() is False,
        QuantumControlPlaneRoot.enable(tenant_id="t1", control_ref="c1").is_missing() is False,
        AutonomousGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        QuantumIntelligenceCoreRoot.enable(tenant_id="t1", intelligence_ref="i1").is_missing() is False,
        ResourceOrchestrationRoot.enable(tenant_id="t1", orchestration_ref="o1").is_missing() is False,
        PolicyEngineBindingRoot.enable(tenant_id="t1", policy_ref="p1").is_missing() is False,
        AgentManagementRoot.enable(tenant_id="t1", agent_ref="a1").is_missing() is False,
        OsKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="kg1").is_missing() is False,
        OsDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_os_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_d", "via_p215_e", "via_p215_f", "via_p215_m", "via_p215_n",
        "via_p215_r", "via_p215_s", "via_p215_k", "via_p215_h", "via_p215_l",
        "via_policy_engine", "via_p213", "via_p214_z", "via_workflow", "via_audit",
        "via_core_platform", "never_replace_core_platform", "never_replace_p215_k",
        "never_replace_p215_h", "module_local_pdp_forbidden", "module_local_llm_forbidden",
        "module_local_quantum_os_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/os")', "/os/control-plane", "/os/orchestration",
        "/os/governance", "/os/intelligence", "/os/policy", "/os/agents",
        "/os/evolution", "/os/knowledge-graph", "/os/digital-twin", "/os/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_OS.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Operating System is missing",
        "Never Quantum Control Plane is missing",
        "Never Autonomous Governance is missing",
        "Never Quantum Intelligence Core is missing",
        "Never Resource Orchestration is missing",
        "Never Policy Engine is missing",
        "Never Agent Management is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "Never Replace Core Platform",
        "Never Replace P215-K Trust Gate",
        "Never Replace P215-H Security Gate",
        "Never Module-Local Policy PDP",
        "MEOS Quantum Operating System SHALL provide",
        "P215-A", "P215-D", "P215-R", "P215-S", "P214-Z", "P213", "Policy Engine",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-T", "adr": 465, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
