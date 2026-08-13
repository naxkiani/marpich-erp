"""Biotechnology P217 foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/499-enterprise-biotechnology-foundation.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_FOUNDATION.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_FOUNDATION_CAPABILITIES.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_FOUNDATION_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_FOUNDATION_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_FOUNDATION_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_FOUNDATION_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_foundation.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_foundation_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_foundation_acl.py",
    "backend/contexts/biotechnology/application/bio_foundation_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/biotechnology_platform",
    "backend/contexts/bio_ai_platform",
    "backend/contexts/synthetic_biology_platform",
    "backend/contexts/digital_health_platform",
)
def validate_bio_foundation_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_foundation_aggregates import (
        BiotechnologyPlatformRoot, SyntheticBiologyRoot, BioAiEngineRoot,
        DigitalHealthRoot, PrecisionMedicineRoot, BiologicalDigitalTwinRoot,
        LifeScienceKnowledgeGraphRoot, BioEthicsGovernanceRoot, BioSecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_foundation as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217" and cat["adr"] == 499 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_bio_intelligence_fabric"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["biotechnology_platform_present_required"] is True
        and cat["synthetic_biology_platform_present_required"] is True
        and cat["bio_ai_intelligence_engine_present_required"] is True
        and cat["digital_health_platform_present_required"] is True
        and cat["precision_medicine_platform_present_required"] is True
        and cat["biological_digital_twin_present_required"] is True
        and cat["life_science_knowledge_graph_present_required"] is True
        and cat["bio_ethics_governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["domain_model"]["entity_count"] == 10
        and cat["never_replace_core_platform"] is True
        and cat["never_replace_ai_platform"] is True
        and cat["never_replace_p215_z"] is True
        and cat["never_replace_robotics_supreme"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["never_replace_laboratory_lims"] is True
        and cat["never_replace_pharmacy"] is True
        and cat["no_module_local_llm"] is True
        and cat["genomic_privacy_required"] is True
        and cat["ethical_bioengineering_required"] is True
        and cat["scientific_reproducibility_required"] is True
        and cat["opaque_bio_safety_decisions_forbidden"] is True
        and cat["bio_ai"]["module_local_llm_forbidden"] is True
        and cat["foundation_for_p217_a"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        BiotechnologyPlatformRoot.enable(tenant_id="t1", bio_ref="b1").is_missing() is False,
        SyntheticBiologyRoot.enable(tenant_id="t1", synthetic_ref="s1").is_missing() is False,
        BioAiEngineRoot.enable(tenant_id="t1", bio_ai_ref="a1").is_missing() is False,
        DigitalHealthRoot.enable(tenant_id="t1", health_ref="h1").is_missing() is False,
        PrecisionMedicineRoot.enable(tenant_id="t1", precision_ref="p1").is_missing() is False,
        BiologicalDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        LifeScienceKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        BioEthicsGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        BioSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_foundation_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p214_z", "via_p215_z", "via_p216_z", "via_p213", "via_identity", "via_policy_engine", "via_workflow",
        "via_audit", "via_integration_platform", "via_search", "via_core_platform",
        "via_hospital_api", "via_laboratory_api", "via_pharmacy_api",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_replace_robotics_supreme", "never_replace_hospital_emr", "never_replace_laboratory_lims",
        "never_replace_pharmacy", "never_replace_identity_platform",
        "module_local_llm_forbidden", "genomic_privacy_required", "ethical_bioengineering_required",
        "scientific_reproducibility_required", "opaque_bio_safety_decisions_forbidden",
        "research_via_integration_platform_only", "module_local_biotechnology_foundation_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/foundation")', "/foundation/vision", "/foundation/domain",
        "/foundation/bounded-contexts", "/foundation/synthetic-biology", "/foundation/bio-ai",
        "/foundation/digital-health", "/foundation/precision-medicine", "/foundation/digital-twin",
        "/foundation/knowledge-graph", "/foundation/governance", "/foundation/observability",
        "/foundation/security", "/foundation/cqrs", "/foundation/events",
        "/foundation/microservices", "/foundation/integration", "/foundation/deployment",
        "/foundation/testing", "/foundation/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_FOUNDATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Biotechnology Platform is missing",
        "Never Synthetic Biology Platform is missing",
        "Never Bio-AI Intelligence Engine is missing",
        "Never Digital Health Platform is missing",
        "Never Precision Medicine Platform is missing",
        "Never Biological Digital Twin is missing",
        "Never Life Science Knowledge Graph is missing",
        "Never Bio Ethics Governance is missing",
        "Never Security Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Bio Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Biotechnology BC",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Hospital EMR SoR",
        "Never Replace Laboratory LIMS SoR",
        "Never Replace Pharmacy SoR",
        "Never Replace Identity Platform",
        "Never Module-Local LLM",
        "Never Skip Genomic Privacy Protections",
        "Never Skip Ethical Bioengineering Review",
        "Never Skip Scientific Reproducibility",
        "Never Skip Human-Centered Health Intelligence",
        "Never Opaque Bio Safety Decisions",
        "MEOS Bio Intelligence Platform SHALL",
        "P214-Z", "P215-Z", "P216-Z", "P217-A",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217", "adr": 499, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
