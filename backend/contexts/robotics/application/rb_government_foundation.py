"""Robotics P216-T government / digital government foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/492-enterprise-robotics-government.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_GOVERNMENT.md",
    "docs/architecture/robotics/ROBOTICS_GOVERNMENT_PUBLIC.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_GOVERNMENT_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_GOVERNMENT_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_GOVERNMENT_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_GOVERNMENT_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_government.py",
    "backend/contexts/robotics/domain/aggregates/rb_government_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_government_acl.py",
    "backend/contexts/robotics/application/rb_government_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/government_robotics_platform",
    "backend/contexts/autonomous_public_service_platform",
    "backend/contexts/digital_government_intelligence_platform",
    "backend/contexts/smart_governance_automation_platform",
)
def validate_rb_government_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_government_aggregates import (
        GovernmentRoboticsRoot, AutonomousPublicServicesRoot, DigitalGovernmentRoot,
        SmartGovernanceRoot, CitizenIntelligenceRoot, PolicyIntelligenceRoot,
        GovernmentDigitalTwinRoot, PublicKnowledgeGraphRoot, GovernmentSecurityRoot,
    )
    from contexts.robotics.domain.services import rb_platform_government as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-T" and cat["adr"] == 492 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_government_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["finance_gate"] == "P216-R"
        and cat["public_safety_gate"] == "P216-L" and cat["physical_ai_gate"] == "P216-E"
        and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["government_robotics_platform_present_required"] is True
        and cat["autonomous_public_services_present_required"] is True
        and cat["digital_government_intelligence_present_required"] is True
        and cat["smart_governance_automation_present_required"] is True
        and cat["citizen_intelligence_platform_present_required"] is True
        and cat["policy_intelligence_platform_present_required"] is True
        and cat["government_digital_twin_present_required"] is True
        and cat["public_knowledge_graph_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["domain_model"]["entity_count"] == 12
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_r_finance"] is True
        and cat["never_replace_identity_platform"] is True
        and cat["never_duplicate_government_core_logic"] is True
        and cat["never_duplicate_municipality_core_logic"] is True
        and cat["no_module_local_llm"] is True
        and cat["privacy_by_design_required"] is True
        and cat["human_governance_oversight_required"] is True
        and cat["explainable_ai_required"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_u"] is True
        and cat["p216_s_legal_planned"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        GovernmentRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        AutonomousPublicServicesRoot.enable(tenant_id="t1", services_ref="s1").is_missing() is False,
        DigitalGovernmentRoot.enable(tenant_id="t1", digital_ref="d1").is_missing() is False,
        SmartGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        CitizenIntelligenceRoot.enable(tenant_id="t1", citizen_ref="c1").is_missing() is False,
        PolicyIntelligenceRoot.enable(tenant_id="t1", policy_ref="p1").is_missing() is False,
        GovernmentDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        PublicKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        GovernmentSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_government_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i", "via_p216_k", "via_p216_l", "via_p216_o", "via_p216_p", "via_p216_q", "via_p216_r",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_government_api", "via_municipality_api", "via_national_id_connector",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_r_finance",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_replace_identity_platform",
        "never_duplicate_government_core_logic", "never_duplicate_municipality_core_logic",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "privacy_by_design_required", "human_governance_oversight_required", "explainable_ai_required",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_government_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/government")', "/government/vision", "/government/domain",
        "/government/bounded-contexts", "/government/robotics", "/government/public-services",
        "/government/digital-government", "/government/smart-governance", "/government/citizen-intelligence",
        "/government/policy-intelligence", "/government/digital-twin", "/government/knowledge-graph",
        "/government/observability", "/government/security", "/government/cqrs", "/government/events",
        "/government/microservices", "/government/integration", "/government/deployment",
        "/government/testing", "/government/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_GOVERNMENT.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Government Robotics Platform is missing",
        "Never Autonomous Public Services is missing",
        "Never Digital Government Intelligence is missing",
        "Never Smart Governance Automation is missing",
        "Never Citizen Intelligence Platform is missing",
        "Never Policy Intelligence Platform is missing",
        "Never Government Digital Twin is missing",
        "Never Public Knowledge Graph is missing",
        "Never Security Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Government Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-R Finance",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Identity Platform",
        "Never Module-Local LLM",
        "Never Duplicate Government Core Logic",
        "Never Duplicate Municipality Core Logic",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Skip Privacy by Design for Citizen Data",
        "Never Skip Human Governance Oversight",
        "Never Skip Explainable AI for Government Decisions",
        "MEOS Government Intelligence Platform SHALL unify",
        "P216", "P216-R", "P215-Z", "P214-Z", "P216-U",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-T", "adr": 492, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
