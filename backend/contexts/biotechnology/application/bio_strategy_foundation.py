"""Biotechnology P217-B strategic architecture foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/501-enterprise-biotechnology-strategic-architecture.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_STRATEGY.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_STRATEGY_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_STRATEGY_CAPABILITIES.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_STRATEGY_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_STRATEGY_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_STRATEGY_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_strategy.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_strategy_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_strategy_acl.py",
    "backend/contexts/biotechnology/application/bio_strategy_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/biotechnology_strategy_platform",
    "backend/contexts/bio_capability_platform",
    "backend/contexts/bio_operating_framework_platform",
)
def validate_bio_strategy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_strategy_aggregates import (
        StrategicArchitectureRoot, CapabilityModelRoot, OperatingFrameworkRoot,
        ServiceModelRoot, OrganizationalModelRoot, GovernanceModelRoot,
        SecurityModelRoot, DataArchitectureRoot, MaturityModelRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_strategy as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-B" and cat["adr"] == 501 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_biotechnology_strategic_architecture_framework"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["biotechnology_strategic_architecture_present_required"] is True
        and cat["capability_model_present_required"] is True
        and cat["operating_framework_present_required"] is True
        and cat["platform_model_present_required"] is True
        and cat["service_model_present_required"] is True
        and cat["organizational_model_present_required"] is True
        and cat["governance_model_present_required"] is True
        and cat["security_model_present_required"] is True
        and cat["data_architecture_present_required"] is True
        and cat["integration_architecture_present_required"] is True
        and cat["scalability_model_present_required"] is True
        and cat["maturity_model_present_required"] is True
        and cat["transformation_roadmap_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["microservices"]["service_count"] >= 8
        and cat["architecture_layers"]["layer_count"] == 5
        and cat["capability_model"]["group_count"] == 6
        and cat["operating_framework"]["component_count"] == 5
        and cat["platform_model"]["team_count"] == 5
        and cat["service_model"]["service_count"] == 16
        and cat["maturity_model"]["level_count"] == 5
        and cat["transformation_roadmap"]["phase_count"] == 4
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_a_mission"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["never_replace_laboratory_lims"] is True
        and cat["never_replace_pharmacy"] is True
        and cat["never_replace_p216_z"] is True
        and cat["genomic_privacy_strategy_required"] is True
        and cat["ethical_bioengineering_strategy_required"] is True
        and cat["scientific_integrity_strategy_required"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_c"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        StrategicArchitectureRoot.enable(tenant_id="t1", architecture_ref="a1").is_missing() is False,
        CapabilityModelRoot.enable(tenant_id="t1", capability_ref="c1").is_missing() is False,
        OperatingFrameworkRoot.enable(tenant_id="t1", framework_ref="f1").is_missing() is False,
        ServiceModelRoot.enable(tenant_id="t1", service_ref="s1").is_missing() is False,
        OrganizationalModelRoot.enable(tenant_id="t1", org_ref="o1").is_missing() is False,
        GovernanceModelRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        SecurityModelRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        DataArchitectureRoot.enable(tenant_id="t1", data_ref="d1").is_missing() is False,
        MaturityModelRoot.enable(tenant_id="t1", maturity_ref="m1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_strategy_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p216_z", "via_p215_z", "via_p214_z", "via_policy_engine", "via_workflow",
        "via_audit", "via_identity", "via_core_platform", "never_replace_p217_foundation",
        "never_replace_p217_a_mission", "never_replace_p215_z", "never_replace_p216_z",
        "never_replace_ai_platform", "never_replace_core_platform", "never_replace_hospital_emr",
        "never_replace_laboratory_lims", "never_replace_pharmacy", "genomic_privacy_strategy_required",
        "ethical_bioengineering_strategy_required", "scientific_integrity_strategy_required",
        "opaque_bio_safety_strategy_forbidden", "module_local_biotechnology_strategy_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/strategy")', "/strategy/layers", "/strategy/capabilities",
        "/strategy/operating-model", "/strategy/services", "/strategy/organization",
        "/strategy/governance", "/strategy/data", "/strategy/integration",
        "/strategy/security", "/strategy/scalability", "/strategy/maturity",
        "/strategy/roadmap", "/strategy/cqrs", "/strategy/events", "/strategy/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_STRATEGY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Biotechnology Strategic Architecture is missing",
        "Never Capability Model is missing",
        "Never Operating Framework is missing",
        "Never Platform Model is missing",
        "Never Service Model is missing",
        "Never Organizational Model is missing",
        "Never Governance Model is missing",
        "Never Security Model is missing",
        "Never Data Architecture is missing",
        "Never Integration Architecture is missing",
        "Never Scalability Model is missing",
        "Never Maturity Model is missing",
        "Never Transformation Roadmap is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Biotechnology BC",
        "Never Replace P217 Foundation",
        "Never Replace P217-A Mission",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Hospital EMR SoR",
        "Never Replace Laboratory LIMS SoR",
        "Never Replace Pharmacy SoR",
        "Never Skip Genomic Privacy Strategy",
        "Never Skip Ethical Bioengineering Strategy",
        "Never Skip Scientific Integrity Strategy",
        "Never Opaque Bio Safety Strategy",
        "MEOS Biotechnology Architecture SHALL",
        "P217", "P217-A", "P216-Z", "P215-Z", "P214-Z", "P217-C",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-B", "adr": 501, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
