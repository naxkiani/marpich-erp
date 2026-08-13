"""Robotics P216-P hospitality / smart hotel foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/488-enterprise-robotics-hospitality.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_HOSPITALITY.md",
    "docs/architecture/robotics/ROBOTICS_HOSPITALITY_HOTEL.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_HOSPITALITY_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_HOSPITALITY_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_HOSPITALITY_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_HOSPITALITY_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_hospitality.py",
    "backend/contexts/robotics/domain/aggregates/rb_hospitality_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_hospitality_acl.py",
    "backend/contexts/robotics/application/rb_hospitality_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/hospitality_robotics_platform",
    "backend/contexts/smart_hotel_platform",
    "backend/contexts/autonomous_guest_service_platform",
    "backend/contexts/hospitality_ai_intelligence_platform",
)
def validate_rb_hospitality_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_hospitality_aggregates import (
        HospitalityRoboticsRoot, SmartHotelRoot, AutonomousGuestServicesRoot,
        GuestExperienceRoot, HospitalityAiRoot, HotelDigitalTwinRoot,
        HospitalityKnowledgeGraphRoot, HospitalitySecurityRoot, RoomIntelligenceRoot,
    )
    from contexts.robotics.domain.services import rb_platform_hospitality as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-P" and cat["adr"] == 488 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_hospitality_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["retail_gate"] == "P216-O"
        and cat["mobility_gate"] == "P216-H" and cat["physical_ai_gate"] == "P216-E"
        and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["hospitality_robotics_platform_present_required"] is True
        and cat["smart_hotel_platform_present_required"] is True
        and cat["autonomous_guest_services_present_required"] is True
        and cat["hospitality_ai_platform_present_required"] is True
        and cat["guest_experience_intelligence_present_required"] is True
        and cat["hotel_digital_twin_present_required"] is True
        and cat["hospitality_knowledge_graph_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["domain_model"]["entity_count"] == 15
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_o_retail"] is True
        and cat["never_direct_payment_bypass"] is True
        and cat["never_duplicate_hotel_pms_core_logic"] is True
        and cat["no_module_local_llm"] is True
        and cat["privacy_by_design_required"] is True
        and cat["human_centered_hospitality_required"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_q"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        HospitalityRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        SmartHotelRoot.enable(tenant_id="t1", hotel_ref="h1").is_missing() is False,
        AutonomousGuestServicesRoot.enable(tenant_id="t1", services_ref="s1").is_missing() is False,
        GuestExperienceRoot.enable(tenant_id="t1", experience_ref="e1").is_missing() is False,
        HospitalityAiRoot.enable(tenant_id="t1", ai_ref="a1").is_missing() is False,
        HotelDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        HospitalityKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        HospitalitySecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        RoomIntelligenceRoot.enable(tenant_id="t1", room_ref="rm1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_hospitality_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i", "via_p216_k", "via_p216_l", "via_p216_o",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_pms_api", "via_booking_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_o_retail",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_direct_payment_bypass", "payment_via_integration_platform_only",
        "never_duplicate_hotel_pms_core_logic",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "privacy_by_design_required", "human_centered_hospitality_required",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_hospitality_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/hospitality")', "/hospitality/vision", "/hospitality/domain",
        "/hospitality/bounded-contexts", "/hospitality/robotics", "/hospitality/smart-hotel",
        "/hospitality/guest-experience", "/hospitality/autonomous-services", "/hospitality/ai",
        "/hospitality/digital-twin", "/hospitality/knowledge-graph", "/hospitality/observability",
        "/hospitality/security", "/hospitality/cqrs", "/hospitality/events", "/hospitality/microservices",
        "/hospitality/integration", "/hospitality/deployment", "/hospitality/testing",
        "/hospitality/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_HOSPITALITY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Hospitality Robotics Platform is missing",
        "Never Smart Hotel Platform is missing",
        "Never Autonomous Guest Services is missing",
        "Never Hospitality AI Platform is missing",
        "Never Guest Experience Intelligence is missing",
        "Never Hotel Digital Twin is missing",
        "Never Hospitality Knowledge Graph is missing",
        "Never Security Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Hospitality Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-O Retail",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Module-Local LLM",
        "Never Duplicate Hotel/PMS Core Logic",
        "Never Direct Payment Bypass of Integration Platform",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Skip Privacy by Design for Guest Data",
        "MEOS Hospitality Intelligence Platform SHALL unify",
        "P216", "P216-O", "P215-Z", "P214-Z", "P216-Q",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-P", "adr": 488, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
