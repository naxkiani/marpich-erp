"""Quantum P215-H security/trust foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/454-enterprise-quantum-security.md",
    "docs/architecture/ENTERPRISE_QUANTUM_SECURITY.md",
    "docs/architecture/quantum/QUANTUM_SECURITY_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_SECURITY_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_SECURITY_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_SECURITY_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_security.py",
    "backend/contexts/quantum/domain/aggregates/qc_security_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_security_acl.py",
    "backend/contexts/quantum/application/qc_security_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_security_platform",
    "backend/contexts/quantum_pqc_platform",
    "backend/contexts/quantum_trust_platform",
    "backend/contexts/post_quantum_platform",
)
def validate_qc_security_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_security_aggregates import (
        QuantumSecurityPlatformRoot, PostQuantumCryptoRoot, QuantumTrustRoot,
        QuantumIdentitySecurityRoot, QuantumKeyManagementRoot, ThreatIntelligenceRoot,
        SecTwinRoot, SecKnowledgeGraphRoot, ZeroTrustRoot,
    )
    from contexts.quantum.domain.services import qc_platform_security as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-H" and cat["adr"] == 454 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["quantum_security_platform_present_required"] is True
        and cat["post_quantum_cryptography_platform_present_required"] is True
        and cat["quantum_trust_architecture_present_required"] is True
        and cat["quantum_identity_security_present_required"] is True
        and cat["quantum_key_management_present_required"] is True
        and cat["threat_intelligence_platform_present_required"] is True
        and cat["pqc_remains_secrets"] is True
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["aggregates"]["aggregate_count"] >= 7
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_d"] is True
        and cat["builds_on_p215_f"] is True and cat["builds_on_p215_g"] is True
        and cat["governed_by_p215_k"] is True
    )
    pqc = PostQuantumCryptoRoot.enable(tenant_id="t1", pqc_ref="p1")
    keys = QuantumKeyManagementRoot.enable(tenant_id="t1", key_ref="k1")
    checks = [
        QuantumSecurityPlatformRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        pqc.is_missing() is False and pqc.pqc_remains_secrets is True,
        QuantumTrustRoot.enable(tenant_id="t1", trust_ref="t1").is_missing() is False,
        QuantumIdentitySecurityRoot.enable(tenant_id="t1", identity_ref="i1").is_missing() is False,
        keys.is_missing() is False and keys.no_local_key_store is True,
        ThreatIntelligenceRoot.enable(tenant_id="t1", threat_ref="th1").is_missing() is False,
        SecTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        SecKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False,
        ZeroTrustRoot.enable(tenant_id="t1", zero_trust_ref="z1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_security_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_d", "via_p215_f", "via_p215_g", "via_p215_k",
        "via_p209", "via_p210", "via_p207", "via_p208", "via_p214_z",
        "pqc_remains_secrets", "module_local_quantum_security_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/security")', "/security/pqc", "/security/identity", "/security/trust",
        "/security/keys", "/security/communication", "/security/threats", "/security/risk",
        "/security/governance", "/security/knowledge-graph", "/security/digital-twin",
        "/security/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_SECURITY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Security Platform is missing",
        "Never Post-Quantum Cryptography Platform is missing",
        "Never Quantum Trust Architecture is missing",
        "Never Quantum Identity Security is missing",
        "Never Quantum Key Management is missing",
        "Never Threat Intelligence Platform is missing",
        "Never Security Knowledge Graph is missing",
        "Never Security Digital Twin is missing",
        "Never Zero Trust Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Security is missing",
        "Never Sibling Quantum BC",
        "Never Local PQC Store",
        "P209", "P215-A", "P215-D",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-H", "adr": 454, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001", "pqc_remains_secrets": True,
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
