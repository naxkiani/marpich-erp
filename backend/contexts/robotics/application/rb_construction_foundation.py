"""Robotics P216-K construction robotics / smart infrastructure foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/483-enterprise-robotics-construction.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_CONSTRUCTION.md",
    "docs/architecture/robotics/ROBOTICS_CONSTRUCTION_SITE.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_CONSTRUCTION_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_CONSTRUCTION_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_CONSTRUCTION_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_CONSTRUCTION_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_construction.py",
    "backend/contexts/robotics/domain/aggregates/rb_construction_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_construction_acl.py",
    "backend/contexts/robotics/application/rb_construction_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/construction_robotics_platform",
    "backend/contexts/smart_infrastructure_platform",
    "backend/contexts/autonomous_building_systems_platform",
    "backend/contexts/digital_construction_intelligence_platform",
)
def validate_rb_construction_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_construction_aggregates import (
        ConstructionRoboticsRoot, SmartInfrastructureRoot, AutonomousBuildingRoot,
        ConstructionAiRoot, ConstructionDigitalTwinRoot, ConstructionKnowledgeGraphRoot,
        ConstructionSecurityRoot, ConstructionManagementRoot, BimManagementRoot,
    )
    from contexts.robotics.domain.services import rb_platform_construction as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-K" and cat["adr"] == 483 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_construction_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["healthcare_gate"] == "P216-I"
        and cat["mobility_gate"] == "P216-H" and cat["physical_ai_gate"] == "P216-E"
        and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["construction_robotics_platform_present_required"] is True
        and cat["smart_infrastructure_platform_present_required"] is True
        and cat["autonomous_building_systems_present_required"] is True
        and cat["construction_ai_present_required"] is True
        and cat["construction_digital_twin_present_required"] is True
        and cat["construction_knowledge_graph_present_required"] is True
        and cat["safety_compliance_architecture_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 6
        and cat["domain_model"]["entity_count"] == 16
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_i_healthcare"] is True
        and cat["never_direct_bim_gis_scada_bypass"] is True
        and cat["never_duplicate_construction_core_logic"] is True
        and cat["no_module_local_llm"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_l"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        ConstructionRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        SmartInfrastructureRoot.enable(tenant_id="t1", infrastructure_ref="i1").is_missing() is False,
        AutonomousBuildingRoot.enable(tenant_id="t1", building_ref="b1").is_missing() is False,
        ConstructionAiRoot.enable(tenant_id="t1", ai_ref="a1").is_missing() is False,
        ConstructionDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        ConstructionKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        ConstructionSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        ConstructionManagementRoot.enable(tenant_id="t1", project_ref="p1").is_missing() is False,
        BimManagementRoot.enable(tenant_id="t1", bim_ref="bim1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_construction_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform", "via_construction_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_i_healthcare",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_direct_bim_gis_scada_bypass", "bim_gis_scada_via_integration_platform_only",
        "never_duplicate_construction_core_logic",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_construction_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/construction")', "/construction/vision", "/construction/domain",
        "/construction/bounded-contexts", "/construction/robotics", "/construction/infrastructure",
        "/construction/buildings", "/construction/ai", "/construction/digital-twin",
        "/construction/knowledge-graph", "/construction/security", "/construction/cqrs",
        "/construction/events", "/construction/microservices", "/construction/integration",
        "/construction/deployment", "/construction/testing", "/construction/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_CONSTRUCTION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Construction Robotics Platform is missing",
        "Never Smart Infrastructure Platform is missing",
        "Never Autonomous Building Systems are missing",
        "Never Construction AI is missing",
        "Never Construction Digital Twin is missing",
        "Never Construction Knowledge Graph is missing",
        "Never Safety & Compliance Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Construction Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-I Healthcare",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Module-Local LLM",
        "Never Duplicate Construction Core Logic",
        "Never Direct BIM/GIS/SCADA Bypass of Integration Platform",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "MEOS Construction Intelligence Platform SHALL unify",
        "P216", "P216-I", "P215-Z", "P214-Z", "P216-L",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-K", "adr": 483, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
