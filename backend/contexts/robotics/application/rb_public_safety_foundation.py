"""Robotics P216-L public safety / civil protection foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/484-enterprise-robotics-public-safety.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_PUBLIC_SAFETY.md",
    "docs/architecture/robotics/ROBOTICS_PUBLIC_SAFETY_INCIDENT.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_PUBLIC_SAFETY_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_PUBLIC_SAFETY_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_PUBLIC_SAFETY_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_PUBLIC_SAFETY_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_public_safety.py",
    "backend/contexts/robotics/domain/aggregates/rb_public_safety_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_public_safety_acl.py",
    "backend/contexts/robotics/application/rb_public_safety_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/public_safety_robotics_platform",
    "backend/contexts/emergency_response_platform",
    "backend/contexts/disaster_recovery_platform",
    "backend/contexts/civil_protection_platform",
)
def validate_rb_public_safety_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_public_safety_aggregates import (
        PublicSafetyRoboticsRoot, EmergencyResponseRoot, DisasterRecoveryRoot,
        CivilProtectionRoot, SituationIntelligenceRoot, DisasterDigitalTwinRoot,
        PublicSafetyKnowledgeGraphRoot, PublicSafetySecurityRoot, MultiRegionResilienceRoot,
    )
    from contexts.robotics.domain.services import rb_platform_public_safety as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-L" and cat["adr"] == 484 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_civil_protection_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["construction_gate"] == "P216-K"
        and cat["healthcare_gate"] == "P216-I" and cat["physical_ai_gate"] == "P216-E"
        and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["public_safety_robotics_platform_present_required"] is True
        and cat["emergency_response_platform_present_required"] is True
        and cat["disaster_recovery_platform_present_required"] is True
        and cat["civil_protection_platform_present_required"] is True
        and cat["disaster_digital_twin_present_required"] is True
        and cat["situation_intelligence_platform_present_required"] is True
        and cat["public_safety_knowledge_graph_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["multi_region_resilience_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 9
        and cat["domain_model"]["entity_count"] == 14
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_k_construction"] is True
        and cat["never_direct_gis_weather_bypass"] is True
        and cat["never_bypass_notification_platform"] is True
        and cat["never_duplicate_hospital_clinic_core_logic"] is True
        and cat["no_module_local_llm"] is True
        and cat["human_centered_explainable_ai_required"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_m"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        PublicSafetyRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        EmergencyResponseRoot.enable(tenant_id="t1", emergency_ref="e1").is_missing() is False,
        DisasterRecoveryRoot.enable(tenant_id="t1", recovery_ref="d1").is_missing() is False,
        CivilProtectionRoot.enable(tenant_id="t1", protection_ref="c1").is_missing() is False,
        SituationIntelligenceRoot.enable(tenant_id="t1", intelligence_ref="i1").is_missing() is False,
        DisasterDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        PublicSafetyKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        PublicSafetySecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        MultiRegionResilienceRoot.enable(tenant_id="t1", resilience_ref="mr1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_public_safety_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i", "via_p216_k",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform", "via_notification_platform",
        "via_hospital_api", "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_k_construction",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_direct_gis_weather_bypass", "gis_weather_via_integration_platform_only",
        "never_bypass_notification_platform", "citizen_alerts_via_notification_platform_only",
        "never_duplicate_hospital_clinic_core_logic",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only", "human_centered_explainable_ai_required",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_public_safety_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/public-safety")', "/public-safety/vision", "/public-safety/domain",
        "/public-safety/bounded-contexts", "/public-safety/robotics", "/public-safety/emergency",
        "/public-safety/recovery", "/public-safety/civil-protection", "/public-safety/intelligence",
        "/public-safety/digital-twin", "/public-safety/knowledge-graph", "/public-safety/observability",
        "/public-safety/security", "/public-safety/cqrs", "/public-safety/events", "/public-safety/microservices",
        "/public-safety/integration", "/public-safety/deployment", "/public-safety/testing",
        "/public-safety/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_PUBLIC_SAFETY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Public Safety Robotics Platform is missing",
        "Never Emergency Response Platform is missing",
        "Never Disaster Recovery Platform is missing",
        "Never Civil Protection Platform is missing",
        "Never Disaster Digital Twin is missing",
        "Never Situation Intelligence Platform is missing",
        "Never Public Safety Knowledge Graph is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Zero Trust Security is missing",
        "Never Multi-Region Resilience is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Public Safety Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-K Construction",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Module-Local LLM",
        "Never Direct GIS/Weather Bypass of Integration Platform",
        "Never Bypass Notification Platform for Citizen Alerts",
        "Never Duplicate Hospital/Clinic Core Logic",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "MEOS Civil Protection Intelligence Platform SHALL unify",
        "P216", "P216-K", "P215-Z", "P214-Z", "P216-M",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-L", "adr": 484, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
