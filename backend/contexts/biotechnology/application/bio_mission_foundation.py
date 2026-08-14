"""Biotechnology P217-A mission / vision / strategy foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/500-enterprise-biotechnology-mission.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_MISSION.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_MISSION_CAPABILITIES.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_MISSION_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_MISSION_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_MISSION_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_MISSION_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_mission.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_mission_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_mission_acl.py",
    "backend/contexts/biotechnology/application/bio_mission_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/biotechnology_mission_platform",
    "backend/contexts/bio_vision_platform",
    "backend/contexts/bio_strategy_platform",
)
def validate_bio_mission_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_mission_aggregates import (
        BiotechnologyMissionRoot, BiotechnologyVisionRoot, StrategicScopeRoot,
        CapabilityFrameworkRoot, ValueStreamsRoot, MaturityModelRoot,
        EvolutionRoadmapRoot, GovernanceStrategyRoot, IntegrationStrategyRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_mission as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-A" and cat["adr"] == 500 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_bio_intelligence_strategic_framework"
        and cat["foundation_gate"] == "P217" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["biotechnology_mission_framework_present_required"] is True
        and cat["biotechnology_vision_framework_present_required"] is True
        and cat["strategic_biotechnology_scope_present_required"] is True
        and cat["bio_capability_framework_present_required"] is True
        and cat["value_streams_framework_present_required"] is True
        and cat["maturity_model_present_required"] is True
        and cat["governance_framework_present_required"] is True
        and cat["meos_integration_strategy_present_required"] is True
        and cat["future_evolution_roadmap_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["microservices"]["service_count"] >= 8
        and cat["objectives"]["objective_count"] >= 7
        and cat["purposes"]["purpose_count"] >= 5
        and cat["bio_domains"]["domain_count"] >= 6
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["never_replace_laboratory_lims"] is True
        and cat["never_replace_pharmacy"] is True
        and cat["never_replace_p216_z"] is True
        and cat["genomic_privacy_strategy_required"] is True
        and cat["ethical_bioengineering_strategy_required"] is True
        and cat["scientific_integrity_strategy_required"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_b"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        BiotechnologyMissionRoot.enable(tenant_id="t1", mission_ref="m1").is_missing() is False,
        BiotechnologyVisionRoot.enable(tenant_id="t1", vision_ref="v1").is_missing() is False,
        StrategicScopeRoot.enable(tenant_id="t1", scope_ref="s1").is_missing() is False,
        CapabilityFrameworkRoot.enable(tenant_id="t1", capability_ref="c1").is_missing() is False,
        ValueStreamsRoot.enable(tenant_id="t1", value_ref="vs1").is_missing() is False,
        MaturityModelRoot.enable(tenant_id="t1", maturity_ref="mm1").is_missing() is False,
        EvolutionRoadmapRoot.enable(tenant_id="t1", roadmap_ref="r1").is_missing() is False,
        GovernanceStrategyRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        IntegrationStrategyRoot.enable(tenant_id="t1", integration_ref="i1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_mission_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p216_z", "via_p215_z", "via_p214_z", "via_policy_engine", "via_workflow",
        "via_audit", "via_identity", "via_core_platform", "never_replace_p217_foundation",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "never_replace_hospital_emr", "never_replace_laboratory_lims",
        "never_replace_pharmacy", "genomic_privacy_strategy_required",
        "ethical_bioengineering_strategy_required", "scientific_integrity_strategy_required",
        "opaque_bio_safety_strategy_forbidden", "module_local_biotechnology_mission_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/mission")', "/mission/vision", "/mission/objectives",
        "/mission/scope", "/mission/capabilities", "/mission/value-streams",
        "/mission/maturity", "/mission/roadmap", "/mission/governance",
        "/mission/integration", "/mission/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_MISSION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Biotechnology Mission Framework is missing",
        "Never Biotechnology Vision Framework is missing",
        "Never Strategic Biotechnology Scope is missing",
        "Never Bio Capability Framework is missing",
        "Never Value Streams Framework is missing",
        "Never Maturity Model is missing",
        "Never Governance Framework is missing",
        "Never MEOS Integration Strategy is missing",
        "Never Future Evolution Roadmap is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Biotechnology BC",
        "Never Replace P217 Foundation",
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
        "Build the world's most advanced enterprise biological intelligence ecosystem",
        "P217", "P216-Z", "P215-Z", "P214-Z", "P217-B",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-A", "adr": 500, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
