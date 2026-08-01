"""Quantum P215-S resilience / cyber defense / zero trust foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/464-enterprise-quantum-resilience.md",
    "docs/architecture/ENTERPRISE_QUANTUM_RESILIENCE.md",
    "docs/architecture/quantum/QUANTUM_RESILIENCE_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_RESILIENCE_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_RESILIENCE_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_RESILIENCE_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_resilience.py",
    "backend/contexts/quantum/domain/aggregates/qc_resilience_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_resilience_acl.py",
    "backend/contexts/quantum/application/qc_resilience_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_security_ops_platform",
    "backend/contexts/quantum_cyber_defense_platform",
    "backend/contexts/quantum_resilience_platform",
    "backend/contexts/quantum_zero_trust_platform",
    "backend/contexts/quantum_identity_security_platform",
)
def validate_qc_resilience_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_resilience_aggregates import (
        QuantumSecurityPlatformRoot, PostQuantumCyberDefenseRoot, QuantumIdentityFabricRoot,
        QuantumZeroTrustRoot, ThreatIntelligenceRoot, SecurityOperationsRoot,
        ResilienceIntelligenceRoot, ResilienceKnowledgeGraphRoot, ResilienceDigitalTwinRoot,
    )
    from contexts.quantum.domain.services import qc_platform_resilience as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-S" and cat["adr"] == 464 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["fabric"] == "meos_quantum_cyber_trust_fabric"
        and cat["security_gate"] == "P215-H"
        and cat["quantum_security_platform_present_required"] is True
        and cat["post_quantum_cyber_defense_present_required"] is True
        and cat["quantum_identity_fabric_present_required"] is True
        and cat["quantum_zero_trust_present_required"] is True
        and cat["threat_intelligence_present_required"] is True
        and cat["security_operations_present_required"] is True
        and cat["resilience_intelligence_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["aggregates"]["aggregate_count"] >= 7
        and cat["microservices"]["service_count"] >= 9
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_h"] is True
        and cat["builds_on_p215_r"] is True and cat["via_p209_secrets"] is True
        and cat["via_identity"] is True and cat["via_policy_engine"] is True
        and cat["never_replace_p215_h"] is True and cat["never_local_pqc_store"] is True
        and cat["pqc_remains_secrets"] is True
        and cat["security_platform"]["never_replace_p215_h"] is True
        and cat["zero_trust"]["module_local_pdp_forbidden"] is True
        and cat["cryptographic_intelligence"]["never_local_pqc_store"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        QuantumSecurityPlatformRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        PostQuantumCyberDefenseRoot.enable(tenant_id="t1", defense_ref="d1").is_missing() is False,
        QuantumIdentityFabricRoot.enable(tenant_id="t1", identity_ref="i1").is_missing() is False,
        QuantumZeroTrustRoot.enable(tenant_id="t1", zero_trust_ref="z1").is_missing() is False,
        ThreatIntelligenceRoot.enable(tenant_id="t1", threat_ref="th1").is_missing() is False,
        SecurityOperationsRoot.enable(tenant_id="t1", soc_ref="soc1").is_missing() is False,
        ResilienceIntelligenceRoot.enable(tenant_id="t1", resilience_ref="r1").is_missing() is False,
        ResilienceKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="kg1").is_missing() is False,
        ResilienceDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_resilience_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_h", "via_p209_secrets", "via_identity", "via_p200_b",
        "via_policy_engine", "via_p214_j", "via_p215_n", "via_p215_k", "via_p215_r",
        "via_p215_l", "via_p215_o", "via_p214_z", "via_workflow", "via_audit",
        "never_replace_p215_h", "never_local_pqc_store", "module_local_pdp_forbidden",
        "module_local_metrics_store_forbidden", "module_local_quantum_resilience_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/resilience")', "/resilience/defense", "/resilience/identity",
        "/resilience/zero-trust", "/resilience/soc", "/resilience/crypto",
        "/resilience/threats", "/resilience/knowledge-graph", "/resilience/digital-twin",
        "/resilience/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_RESILIENCE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Security Platform is missing",
        "Never Post-Quantum Cyber Defense is missing",
        "Never Quantum Identity Fabric is missing",
        "Never Quantum Zero Trust is missing",
        "Never Threat Intelligence is missing",
        "Never Security Operations is missing",
        "Never Resilience Intelligence is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "Never Replace P215-H Security Gate",
        "Never Local PQC Store",
        "MEOS Quantum Security Platform SHALL provide",
        "P215-A", "P215-H", "P215-R", "P209", "P200-B", "Policy Engine", "P214-J",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-S", "adr": 464, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
