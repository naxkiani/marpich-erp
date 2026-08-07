"""Space P218-G Orbital Intelligence foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/533-enterprise-space-intelligence-orbital.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_ORBITAL.md",
    "docs/architecture/space/ORBITAL_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/ORBITAL_SSA.v1.yaml",
    "docs/architecture/space/ORBITAL_DDD_CQRS.v1.yaml",
    "docs/architecture/space/ORBITAL_SECURITY.v1.yaml",
    "docs/architecture/space/ORBITAL_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_orbital.py",
    "backend/contexts/space/domain/aggregates/sp_orbital_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_orbital_acl.py",
    "backend/contexts/space/application/sp_orbital_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/orbital_intelligence_platform",
    "backend/contexts/ssa_platform_bc",
    "backend/contexts/collision_avoidance_bc",
)
def validate_sp_orbital_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_orbital_aggregates import (
        OrbitalPlatformRoot, SsaRoot, TrafficRoot, CollisionAvoidanceRoot, DebrisIntelligenceRoot,
        OrbitalDigitalTwinRoot, OrbitalKnowledgeGraphRoot, OrbitalAiAutonomyRoot, OrbitalSecurityRoot,
    )
    from contexts.space.domain.services import sp_platform_orbital as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-G" and cat["adr"] == 533 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_orbital_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["satellite_gate"] == "P218-F"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_situational_awareness_present_required"] is True
        and cat["orbital_traffic_management_present_required"] is True
        and cat["collision_avoidance_present_required"] is True
        and cat["space_debris_intelligence_present_required"] is True
        and cat["orbital_digital_twin_present_required"] is True
        and cat["orbital_knowledge_graph_present_required"] is True
        and cat["ai_autonomy_present_required"] is True
        and cat["ddd_model_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["deployment_architecture_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["ssa"]["capability_count"] == 8
        and cat["ssa"]["category_count"] == 8
        and cat["collision_avoidance"]["pipeline_step_count"] == 9
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 12
        and cat["never_replace_p218_foundation"] is True
        and cat["never_replace_p218_f_satellite"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["no_module_local_ssa_sensor_stack"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["never_ungated_collision_avoidance_maneuver"] is True
        and cat["never_disable_human_override"] is True
        and cat["foundation_for_p218_h"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        OrbitalPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        SsaRoot.enable(tenant_id="t1", ssa_ref="s1").is_missing() is False,
        TrafficRoot.enable(tenant_id="t1", traffic_ref="t1").is_missing() is False,
        CollisionAvoidanceRoot.enable(tenant_id="t1", avoidance_ref="a1").is_missing() is False,
        DebrisIntelligenceRoot.enable(tenant_id="t1", debris_ref="d1").is_missing() is False,
        OrbitalDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        OrbitalKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        OrbitalAiAutonomyRoot.enable(tenant_id="t1", ai_ref="ai1").is_missing() is False,
        OrbitalSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_orbital_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p218", "via_p218_a", "via_p218_b", "via_p218_c", "via_p218_d", "via_p218_e", "via_p218_f",
        "via_p217", "via_p216_z", "via_p215_z", "via_p214_z", "via_integration",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p218_foundation", "never_replace_p218_f_satellite",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "never_replace_biotechnology",
        "space_ai_via_p214z_acl_only", "no_module_local_llm", "no_module_local_ssa_sensor_stack",
        "never_opaque_unexplainable_decisions", "never_ungated_collision_avoidance_maneuver",
        "never_disable_human_override", "module_local_orbital_forbidden",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/orbital")', "/orbital/vision", "/orbital/architecture",
        "/orbital/ssa", "/orbital/traffic", "/orbital/collision-avoidance",
        "/orbital/debris", "/orbital/digital-twin", "/orbital/knowledge-graph",
        "/orbital/ai-autonomy", "/orbital/observability", "/orbital/governance",
        "/orbital/security", "/orbital/integration", "/orbital/deployment",
        "/orbital/testing", "/orbital/cqrs", "/orbital/events", "/orbital/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_ORBITAL.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Situational Awareness is missing",
        "Never Orbital Traffic Management is missing",
        "Never Collision Avoidance is missing",
        "Never Space Debris Intelligence is missing",
        "Never Orbital Digital Twin is missing",
        "Never Orbital Knowledge Graph is missing",
        "Never AI Autonomy is missing",
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
        "Never Replace P218-F Satellite",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Biotechnology (P217)",
        "Never Module-Local LLM",
        "Never Module-Local Telemetry Stack",
        "Never Module-Local SSA Sensor Stack",
        "Never Opaque Unexplainable Decisions",
        "Never Skip Human Mission Oversight Strategy",
        "Never Skip Space Cybersecurity Strategy",
        "Never Skip Space Sustainability Strategy",
        "Never Opaque Mission-Critical Strategy",
        "Never Ungated Autonomous Mission Strategy",
        "Never Ungated Satellite Command Uplink",
        "Never Ungated Collision Avoidance Maneuver",
        "Never Disable Human Override",
        "continuous, global, real-time awareness",
        "P218", "P218-F", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "P218-H",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-G", "adr": 533, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
