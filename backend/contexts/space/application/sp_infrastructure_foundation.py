"""Space P218-D infrastructure foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/530-enterprise-space-intelligence-infrastructure.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_INFRASTRUCTURE.md",
    "docs/architecture/space/SPACE_INFRASTRUCTURE_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/SPACE_INFRASTRUCTURE_COMPUTE.v1.yaml",
    "docs/architecture/space/SPACE_INFRASTRUCTURE_DDD_CQRS.v1.yaml",
    "docs/architecture/space/SPACE_INFRASTRUCTURE_SECURITY.v1.yaml",
    "docs/architecture/space/SPACE_INFRASTRUCTURE_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_infrastructure.py",
    "backend/contexts/space/domain/aggregates/sp_infrastructure_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_infrastructure_acl.py",
    "backend/contexts/space/application/sp_infrastructure_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_infrastructure_platform",
    "backend/contexts/space_cloud_platform",
    "backend/contexts/ground_segment_platform_bc",
)
def validate_sp_infrastructure_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_infrastructure_aggregates import (
        SpaceInfrastructureRoot, GroundSegmentRoot, MissionControlRoot, SpaceCloudRoot,
        SpaceNetworkRoot, SpaceDataInfraRoot, InfraDigitalTwinRoot, InfraSecurityRoot, ObservabilityRoot,
    )
    from contexts.space.domain.services import sp_platform_infrastructure as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-D" and cat["adr"] == 530 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_intelligence_infrastructure_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_infrastructure_architecture_present_required"] is True
        and cat["ground_segment_platform_present_required"] is True
        and cat["mission_control_platform_present_required"] is True
        and cat["space_cloud_platform_present_required"] is True
        and cat["space_network_architecture_present_required"] is True
        and cat["space_data_platform_present_required"] is True
        and cat["infrastructure_digital_twin_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["observability_architecture_present_required"] is True
        and cat["disaster_recovery_present_required"] is True
        and cat["container_platform_architecture_present_required"] is True
        and cat["deployment_model_present_required"] is True
        and cat["testing_architecture_present_required"] is True
        and cat["infrastructure_layers"]["layer_count"] == 5
        and cat["ground_segment"]["component_count"] == 9
        and cat["space_cloud"]["component_count"] == 6
        and cat["data_infrastructure"]["domain_count"] == 4
        and cat["storage_architecture"]["type_count"] == 4
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_foundation"] is True
        and cat["never_replace_p218_c_domain"] is True
        and cat["module_local_observability_store_forbidden"] is True
        and cat["never_direct_ground_station_bypass_of_integration_platform"] is True
        and cat["never_opaque_mission_critical_strategy"] is True
        and cat["never_ungated_autonomous_mission_strategy"] is True
        and cat["foundation_for_p218_e"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        SpaceInfrastructureRoot.enable(tenant_id="t1", infra_ref="i1").is_missing() is False,
        GroundSegmentRoot.enable(tenant_id="t1", ground_ref="g1").is_missing() is False,
        MissionControlRoot.enable(tenant_id="t1", moc_ref="m1").is_missing() is False,
        SpaceCloudRoot.enable(tenant_id="t1", cloud_ref="c1").is_missing() is False,
        SpaceNetworkRoot.enable(tenant_id="t1", network_ref="n1").is_missing() is False,
        SpaceDataInfraRoot.enable(tenant_id="t1", data_ref="d1").is_missing() is False,
        InfraDigitalTwinRoot.enable(tenant_id="t1", twin_ref="t1").is_missing() is False,
        InfraSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        ObservabilityRoot.enable(tenant_id="t1", observability_ref="o1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_infrastructure_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p218", "via_p218_a", "via_p218_b", "via_p218_c", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_observability_platform",
        "via_integration_platform", "via_core_platform", "never_replace_p218_foundation",
        "never_replace_p218_a_mission", "never_replace_p218_b_strategy", "never_replace_p218_c_domain",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "never_replace_biotechnology",
        "module_local_space_infrastructure_forbidden",
        "never_direct_ground_station_bypass_of_integration_platform",
        "module_local_observability_store_forbidden",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/infrastructure")', "/infrastructure/layers",
        "/infrastructure/ground-segment", "/infrastructure/mission-control", "/infrastructure/cloud",
        "/infrastructure/network", "/infrastructure/data", "/infrastructure/digital-twin",
        "/infrastructure/security", "/infrastructure/platform", "/infrastructure/observability",
        "/infrastructure/resilience", "/infrastructure/integration", "/infrastructure/deployment",
        "/infrastructure/testing", "/infrastructure/cqrs", "/infrastructure/events",
        "/infrastructure/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_INFRASTRUCTURE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Infrastructure Architecture is missing",
        "Never Ground Segment Platform is missing",
        "Never Mission Control Platform is missing",
        "Never Space Cloud Platform is missing",
        "Never Space Network Architecture is missing",
        "Never Space Data Platform is missing",
        "Never Infrastructure Digital Twin is missing",
        "Never Infrastructure Security is missing",
        "Never Observability Architecture is missing",
        "Never Disaster Recovery is missing",
        "Never Container Platform Architecture is missing",
        "Never Deployment Model is missing",
        "Never Testing Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Sibling Space BC",
        "Never Replace P218 Foundation",
        "Never Replace P218-A Mission",
        "Never Replace P218-B Strategy",
        "Never Replace P218-C Domain",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Biotechnology (P217)",
        "Never Skip Human Mission Oversight Strategy",
        "Never Skip Space Cybersecurity Strategy",
        "Never Skip Space Sustainability Strategy",
        "Never Opaque Mission-Critical Strategy",
        "Never Ungated Autonomous Mission Strategy",
        "Never Module-Local Observability Store",
        "Never Direct Ground Station Bypass of Integration Platform",
        "Provide a secure",
        "P218", "P218-A", "P218-B", "P218-C", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "P218-E",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-D", "adr": 530, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
