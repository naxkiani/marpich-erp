"""Space P218-F Satellite Intelligence foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/532-enterprise-space-intelligence-satellite.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_SATELLITE.md",
    "docs/architecture/space/SATELLITE_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/SATELLITE_LIFECYCLE.v1.yaml",
    "docs/architecture/space/SATELLITE_DDD_CQRS.v1.yaml",
    "docs/architecture/space/SATELLITE_SECURITY.v1.yaml",
    "docs/architecture/space/SATELLITE_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_satellite.py",
    "backend/contexts/space/domain/aggregates/sp_satellite_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_satellite_acl.py",
    "backend/contexts/space/application/sp_satellite_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/satellite_intelligence_platform",
    "backend/contexts/constellation_management_bc",
    "backend/contexts/orbital_asset_platform_bc",
)
def validate_sp_satellite_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_satellite_aggregates import (
        SatellitePlatformRoot, ConstellationRoot, OrbitalAssetRoot, SatelliteLifecycleRoot,
        PayloadIntelligenceRoot, SatelliteAiRoot, SatelliteDigitalTwinRoot, SatelliteGovernanceRoot, SatelliteSecurityRoot,
    )
    from contexts.space.domain.services import sp_platform_satellite as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-F" and cat["adr"] == 532 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_satellite_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["satellite_intelligence_platform_present_required"] is True
        and cat["constellation_management_present_required"] is True
        and cat["orbital_asset_operations_present_required"] is True
        and cat["satellite_lifecycle_present_required"] is True
        and cat["payload_intelligence_present_required"] is True
        and cat["satellite_ai_present_required"] is True
        and cat["satellite_digital_twin_present_required"] is True
        and cat["ddd_model_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["deployment_architecture_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["phase_count"] == 10
        and cat["constellation"]["capability_count"] == 10
        and cat["constellation"]["type_count"] == 8
        and cat["satellite_ai"]["model_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 11
        and cat["never_replace_p218_foundation"] is True
        and cat["never_replace_p218_e_space_ai"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["no_module_local_telemetry_stack"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_ungated_autonomous_mission_strategy"] is True
        and cat["never_ungated_satellite_command_uplink"] is True
        and cat["foundation_for_p218_g"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        SatellitePlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        ConstellationRoot.enable(tenant_id="t1", constellation_ref="c1").is_missing() is False,
        OrbitalAssetRoot.enable(tenant_id="t1", asset_ref="a1").is_missing() is False,
        SatelliteLifecycleRoot.enable(tenant_id="t1", lifecycle_ref="l1").is_missing() is False,
        PayloadIntelligenceRoot.enable(tenant_id="t1", payload_ref="pl1").is_missing() is False,
        SatelliteAiRoot.enable(tenant_id="t1", ai_ref="ai1").is_missing() is False,
        SatelliteDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        SatelliteGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        SatelliteSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_satellite_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p218", "via_p218_a", "via_p218_b", "via_p218_c", "via_p218_d", "via_p218_e",
        "via_p217", "via_p216_z", "via_p215_z", "via_p214_z", "via_integration",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p218_foundation", "never_replace_p218_e_space_ai",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "never_replace_biotechnology",
        "space_ai_via_p214z_acl_only", "no_module_local_llm", "no_module_local_telemetry_stack",
        "never_opaque_unexplainable_decisions", "never_ungated_satellite_command_uplink",
        "module_local_satellite_forbidden",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/satellite")', "/satellite/vision", "/satellite/architecture",
        "/satellite/lifecycle", "/satellite/constellation", "/satellite/orbital-assets",
        "/satellite/payload", "/satellite/satellite-ai", "/satellite/digital-twin",
        "/satellite/observability", "/satellite/governance", "/satellite/security",
        "/satellite/integration", "/satellite/deployment", "/satellite/testing",
        "/satellite/cqrs", "/satellite/events", "/satellite/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_SATELLITE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Satellite Intelligence Platform is missing",
        "Never Constellation Management Platform is missing",
        "Never Orbital Asset Operations is missing",
        "Never Satellite Lifecycle is missing",
        "Never Payload Intelligence is missing",
        "Never Satellite AI is missing",
        "Never Satellite Digital Twin is missing",
        "Never DDD Model is missing",
        "Never Security Architecture is missing",
        "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Sibling Space BC",
        "Never Replace P218 Foundation",
        "Never Replace P218-A Mission",
        "Never Replace P218-B Strategy",
        "Never Replace P218-C Domain",
        "Never Replace P218-D Infrastructure",
        "Never Replace P218-E Space AI",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Biotechnology (P217)",
        "Never Module-Local LLM",
        "Never Module-Local Telemetry Stack",
        "Never Opaque Unexplainable Decisions",
        "Never Skip Human Mission Oversight Strategy",
        "Never Skip Space Cybersecurity Strategy",
        "Never Skip Space Sustainability Strategy",
        "Never Opaque Mission-Critical Strategy",
        "Never Ungated Autonomous Mission Strategy",
        "Never Ungated Satellite Command Uplink",
        "thousands of satellites",
        "P218", "P218-E", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "P218-G",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-F", "adr": 532, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
