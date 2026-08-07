"""Space P218-H Space Communications foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/534-enterprise-space-intelligence-communications.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_COMMUNICATIONS.md",
    "docs/architecture/space/COMMUNICATIONS_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/COMMUNICATIONS_DSN.v1.yaml",
    "docs/architecture/space/COMMUNICATIONS_DDD_CQRS.v1.yaml",
    "docs/architecture/space/COMMUNICATIONS_SECURITY.v1.yaml",
    "docs/architecture/space/COMMUNICATIONS_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_communications.py",
    "backend/contexts/space/domain/aggregates/sp_communications_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_communications_acl.py",
    "backend/contexts/space/application/sp_communications_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_communications_platform",
    "backend/contexts/deep_space_network_bc",
    "backend/contexts/laser_communications_bc",
)
def validate_sp_communications_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_communications_aggregates import (
        CommunicationsPlatformRoot, DeepSpaceNetworkRoot, InterSatelliteNetworkRoot, LaserCommunicationsRoot,
        NetworkAiRoot, CommunicationsDigitalTwinRoot, MissionCommsRoot, CommunicationsObservabilityRoot, CommunicationsSecurityRoot,
    )
    from contexts.space.domain.services import sp_platform_communications as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-H" and cat["adr"] == 534 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_communications_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["satellite_gate"] == "P218-F" and cat["orbital_gate"] == "P218-G"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_communications_platform_present_required"] is True
        and cat["deep_space_network_present_required"] is True
        and cat["inter_satellite_networking_present_required"] is True
        and cat["laser_communications_present_required"] is True
        and cat["communication_ai_platform_present_required"] is True
        and cat["communication_digital_twin_present_required"] is True
        and cat["ddd_model_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["observability_present_required"] is True
        and cat["deployment_architecture_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["architecture"]["dtn_native"] is True
        and cat["dsn"]["capability_count"] == 8
        and cat["inter_satellite"]["capability_count"] == 8
        and cat["laser"]["capability_count"] == 8
        and cat["network_ai"]["model_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_foundation"] is True
        and cat["never_replace_p218_g_orbital"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["no_module_local_communications_radio_stack"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_ungated_command_transport"] is True
        and cat["never_skip_delay_tolerant_networking"] is True
        and cat["foundation_for_p218_i"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CommunicationsPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        DeepSpaceNetworkRoot.enable(tenant_id="t1", dsn_ref="d1").is_missing() is False,
        InterSatelliteNetworkRoot.enable(tenant_id="t1", isn_ref="i1").is_missing() is False,
        LaserCommunicationsRoot.enable(tenant_id="t1", laser_ref="l1").is_missing() is False,
        NetworkAiRoot.enable(tenant_id="t1", ai_ref="a1").is_missing() is False,
        CommunicationsDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        MissionCommsRoot.enable(tenant_id="t1", mission_ref="m1").is_missing() is False,
        CommunicationsObservabilityRoot.enable(tenant_id="t1", obs_ref="o1").is_missing() is False,
        CommunicationsSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_communications_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p218", "via_p218_a", "via_p218_b", "via_p218_c", "via_p218_d", "via_p218_e", "via_p218_f", "via_p218_g",
        "via_p217", "via_p216_z", "via_p215_z", "via_p214_z", "via_integration",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p218_foundation", "never_replace_p218_g_orbital",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "never_replace_biotechnology",
        "space_ai_via_p214z_acl_only", "no_module_local_llm", "no_module_local_communications_radio_stack",
        "never_opaque_unexplainable_decisions", "never_ungated_command_transport",
        "never_skip_delay_tolerant_networking", "module_local_communications_forbidden", "quantum_ready",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/communications")', "/communications/vision", "/communications/architecture",
        "/communications/dsn", "/communications/inter-satellite", "/communications/laser",
        "/communications/mission-services", "/communications/network-ai", "/communications/digital-twin",
        "/communications/observability", "/communications/governance", "/communications/security",
        "/communications/integration", "/communications/deployment", "/communications/testing",
        "/communications/cqrs", "/communications/events", "/communications/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_COMMUNICATIONS.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Communications Platform is missing",
        "Never Deep Space Network is missing",
        "Never Inter-Satellite Networking is missing",
        "Never Laser Communications is missing",
        "Never Communication AI Platform is missing",
        "Never Communication Digital Twin is missing",
        "Never DDD Model is missing",
        "Never Security Architecture is missing",
        "Never Observability is missing",
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
        "Never Replace P218-F Satellite",
        "Never Replace P218-G Orbital",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Biotechnology (P217)",
        "Never Module-Local LLM",
        "Never Module-Local Telemetry Stack",
        "Never Module-Local Communications Radio Stack",
        "Never Opaque Unexplainable Decisions",
        "Never Skip Human Mission Oversight Strategy",
        "Never Skip Space Cybersecurity Strategy",
        "Never Skip Space Sustainability Strategy",
        "Never Opaque Mission-Critical Strategy",
        "Never Ungated Autonomous Mission Strategy",
        "Never Ungated Satellite Command Uplink",
        "Never Ungated Collision Avoidance Maneuver",
        "Never Ungated Command Transport",
        "Never Disable Human Override",
        "Never Skip Delay-Tolerant Networking",
        "secure, resilient, autonomous, high-bandwidth communications",
        "P218", "P218-G", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "P218-I",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-H", "adr": 534, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
