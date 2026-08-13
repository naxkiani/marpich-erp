"""Biotechnology P217-D infrastructure foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/503-enterprise-biotechnology-infrastructure.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_INFRASTRUCTURE.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_INFRASTRUCTURE_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_INFRASTRUCTURE_COMPUTE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_INFRASTRUCTURE_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_INFRASTRUCTURE_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_INFRASTRUCTURE_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_infrastructure.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_infrastructure_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_infrastructure_acl.py",
    "backend/contexts/biotechnology/application/bio_infrastructure_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/biotechnology_infrastructure_platform",
    "backend/contexts/bio_cloud_platform",
    "backend/contexts/scientific_computing_platform_bc",
)
def validate_bio_infrastructure_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_infrastructure_aggregates import (
        BioInfrastructureRoot, ScientificComputingRoot, BioCloudRoot, BioDataInfraRoot,
        AiComputeRoot, LaboratoryIntegrationRoot, InfraSecurityRoot, ObservabilityRoot, ResilienceRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_infrastructure as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-D" and cat["adr"] == 503 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_bio_intelligence_infrastructure_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["bio_infrastructure_architecture_present_required"] is True
        and cat["scientific_computing_platform_present_required"] is True
        and cat["bio_cloud_architecture_present_required"] is True
        and cat["data_infrastructure_present_required"] is True
        and cat["ai_compute_foundation_present_required"] is True
        and cat["laboratory_integration_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["observability_architecture_present_required"] is True
        and cat["disaster_recovery_present_required"] is True
        and cat["container_platform_architecture_present_required"] is True
        and cat["deployment_model_present_required"] is True
        and cat["testing_architecture_present_required"] is True
        and cat["infrastructure_layers"]["layer_count"] == 5
        and cat["scientific_computing"]["component_count"] == 3
        and cat["bio_cloud"]["component_count"] == 4
        and cat["data_infrastructure"]["domain_count"] == 4
        and cat["storage_architecture"]["type_count"] == 4
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_c_domain"] is True
        and cat["module_local_observability_store_forbidden"] is True
        and cat["never_direct_lab_hardware_bypass_of_integration_platform"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_e"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        BioInfrastructureRoot.enable(tenant_id="t1", infra_ref="i1").is_missing() is False,
        ScientificComputingRoot.enable(tenant_id="t1", compute_ref="c1").is_missing() is False,
        BioCloudRoot.enable(tenant_id="t1", cloud_ref="cl1").is_missing() is False,
        BioDataInfraRoot.enable(tenant_id="t1", data_ref="d1").is_missing() is False,
        AiComputeRoot.enable(tenant_id="t1", ai_compute_ref="a1").is_missing() is False,
        LaboratoryIntegrationRoot.enable(tenant_id="t1", lab_ref="l1").is_missing() is False,
        InfraSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        ObservabilityRoot.enable(tenant_id="t1", observability_ref="o1").is_missing() is False,
        ResilienceRoot.enable(tenant_id="t1", resilience_ref="r1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_infrastructure_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_observability_platform",
        "via_integration_platform", "via_core_platform", "never_replace_p217_foundation",
        "never_replace_p217_a_mission", "never_replace_p217_b_strategy", "never_replace_p217_c_domain",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "opaque_bio_safety_strategy_forbidden",
        "module_local_biotechnology_infrastructure_forbidden",
        "never_direct_lab_hardware_bypass_of_integration_platform",
        "module_local_observability_store_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/infrastructure")', "/infrastructure/layers",
        "/infrastructure/scientific-computing", "/infrastructure/cloud", "/infrastructure/data",
        "/infrastructure/storage", "/infrastructure/ai-compute", "/infrastructure/laboratory",
        "/infrastructure/security", "/infrastructure/platform", "/infrastructure/observability",
        "/infrastructure/resilience", "/infrastructure/integration", "/infrastructure/deployment",
        "/infrastructure/testing", "/infrastructure/cqrs", "/infrastructure/events",
        "/infrastructure/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_INFRASTRUCTURE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Bio Infrastructure Architecture is missing",
        "Never Scientific Computing Platform is missing",
        "Never Bio Cloud Architecture is missing",
        "Never Data Infrastructure is missing",
        "Never AI Compute Foundation is missing",
        "Never Laboratory Integration is missing",
        "Never Security Architecture is missing",
        "Never Observability Architecture is missing",
        "Never Disaster Recovery is missing",
        "Never Container Platform Architecture is missing",
        "Never Deployment Model is missing",
        "Never Testing Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Sibling Biotechnology BC",
        "Never Replace P217 Foundation",
        "Never Replace P217-A Mission",
        "Never Replace P217-B Strategy",
        "Never Replace P217-C Domain",
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
        "Never Module-Local Observability Store",
        "Never Direct Lab Hardware Bypass of Integration Platform",
        "Provide a secure",
        "P217", "P217-A", "P217-B", "P217-C", "P216-Z", "P215-Z", "P214-Z", "P217-E",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-D", "adr": 503, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
