"""Space P218-I Space Navigation foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/535-enterprise-space-intelligence-navigation.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_NAVIGATION.md",
    "docs/architecture/space/NAVIGATION_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/NAVIGATION_GNSS.v1.yaml",
    "docs/architecture/space/NAVIGATION_DDD_CQRS.v1.yaml",
    "docs/architecture/space/NAVIGATION_SECURITY.v1.yaml",
    "docs/architecture/space/NAVIGATION_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_navigation.py",
    "backend/contexts/space/domain/aggregates/sp_navigation_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_navigation_acl.py",
    "backend/contexts/space/application/sp_navigation_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_navigation_platform",
    "backend/contexts/gnss_intelligence_bc",
    "backend/contexts/gnc_platform_bc",
)
def validate_sp_navigation_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_navigation_aggregates import (
        NavigationPlatformRoot, GnssIntelligenceRoot, AutonomousNavigationRoot, TrajectoryOptimizationRoot,
        GncRoot, NavigationAiRoot, NavigationDigitalTwinRoot, NavigationObservabilityRoot, NavigationSecurityRoot,
    )
    from contexts.space.domain.services import sp_platform_navigation as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-I" and cat["adr"] == 535 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_navigation_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["satellite_gate"] == "P218-F" and cat["orbital_gate"] == "P218-G"
        and cat["communications_gate"] == "P218-H"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_navigation_platform_present_required"] is True
        and cat["gnss_intelligence_present_required"] is True
        and cat["autonomous_navigation_present_required"] is True
        and cat["trajectory_optimization_present_required"] is True
        and cat["guidance_and_control_present_required"] is True
        and cat["navigation_ai_present_required"] is True
        and cat["navigation_digital_twin_present_required"] is True
        and cat["ddd_model_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["observability_present_required"] is True
        and cat["deployment_architecture_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["gnss"]["capability_count"] == 8
        and cat["gnss"]["system_count"] == 7
        and cat["navigation_ai"]["model_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_foundation"] is True
        and cat["never_replace_p218_h_communications"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["no_module_local_gnss_receiver_stack"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_ungated_guidance_command"] is True
        and cat["never_skip_gnss_spoofing_detection"] is True
        and cat["foundation_for_p218_j"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        NavigationPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        GnssIntelligenceRoot.enable(tenant_id="t1", gnss_ref="g1").is_missing() is False,
        AutonomousNavigationRoot.enable(tenant_id="t1", autonav_ref="a1").is_missing() is False,
        TrajectoryOptimizationRoot.enable(tenant_id="t1", trajectory_ref="tr1").is_missing() is False,
        GncRoot.enable(tenant_id="t1", gnc_ref="gnc1").is_missing() is False,
        NavigationAiRoot.enable(tenant_id="t1", ai_ref="ai1").is_missing() is False,
        NavigationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        NavigationObservabilityRoot.enable(tenant_id="t1", obs_ref="o1").is_missing() is False,
        NavigationSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_navigation_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p218", "via_p218_a", "via_p218_b", "via_p218_c", "via_p218_d", "via_p218_e", "via_p218_f", "via_p218_g", "via_p218_h",
        "via_p217", "via_p216_z", "via_p215_z", "via_p214_z", "via_integration",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p218_foundation", "never_replace_p218_h_communications",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "never_replace_biotechnology",
        "space_ai_via_p214z_acl_only", "no_module_local_llm", "no_module_local_gnss_receiver_stack",
        "never_opaque_unexplainable_decisions", "never_ungated_guidance_command",
        "never_skip_gnss_spoofing_detection", "module_local_navigation_forbidden",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/navigation")', "/navigation/vision", "/navigation/architecture",
        "/navigation/gnss", "/navigation/autonomous", "/navigation/trajectory",
        "/navigation/gnc", "/navigation/navigation-ai", "/navigation/digital-twin",
        "/navigation/observability", "/navigation/governance", "/navigation/security",
        "/navigation/integration", "/navigation/deployment", "/navigation/testing",
        "/navigation/cqrs", "/navigation/events", "/navigation/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_NAVIGATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Navigation Platform is missing",
        "Never GNSS Intelligence is missing",
        "Never Autonomous Navigation is missing",
        "Never Trajectory Optimization is missing",
        "Never Guidance & Control is missing",
        "Never Navigation AI is missing",
        "Never Navigation Digital Twin is missing",
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
        "Never Replace P218-H Communications",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Biotechnology (P217)",
        "Never Module-Local LLM",
        "Never Module-Local Telemetry Stack",
        "Never Module-Local Communications Radio Stack",
        "Never Module-Local GNSS Receiver Stack",
        "Never Opaque Unexplainable Decisions",
        "Never Skip Human Mission Oversight Strategy",
        "Never Skip Space Cybersecurity Strategy",
        "Never Skip Space Sustainability Strategy",
        "Never Opaque Mission-Critical Strategy",
        "Never Ungated Autonomous Mission Strategy",
        "Never Ungated Satellite Command Uplink",
        "Never Ungated Collision Avoidance Maneuver",
        "Never Ungated Command Transport",
        "Never Ungated Guidance Command",
        "Never Disable Human Override",
        "Never Skip Delay-Tolerant Networking",
        "Never Skip GNSS Spoofing Detection",
        "unified navigation intelligence platform",
        "P218", "P218-H", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "P218-J",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-I", "adr": 535, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
