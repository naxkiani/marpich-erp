"""Robotics P216-F industrial / smart factory foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/478-enterprise-robotics-industrial.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_INDUSTRIAL.md",
    "docs/architecture/robotics/ROBOTICS_INDUSTRIAL_FACTORY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_INDUSTRIAL_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_INDUSTRIAL_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_INDUSTRIAL_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_INDUSTRIAL_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_industrial.py",
    "backend/contexts/robotics/domain/aggregates/rb_industrial_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_industrial_acl.py",
    "backend/contexts/robotics/application/rb_industrial_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/smart_factory_platform",
    "backend/contexts/industrial_automation_platform",
    "backend/contexts/manufacturing_intelligence_platform",
)
def validate_rb_industrial_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_industrial_aggregates import (
        SmartFactoryRoot, IndustrialAutomationRoot, AutonomousManufacturingRoot,
        ManufacturingExecutionRoot, FactoryDigitalTwinRoot, PredictiveMaintenanceRoot,
        IndustrialKnowledgeGraphRoot, IndustrialCybersecurityRoot, IndustrialAnalyticsRoot,
    )
    from contexts.robotics.domain.services import rb_platform_industrial as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-F" and cat["adr"] == 478 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_industrial_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["physical_ai_gate"] == "P216-E"
        and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["smart_factory_platform_present_required"] is True
        and cat["industrial_automation_platform_present_required"] is True
        and cat["autonomous_manufacturing_platform_present_required"] is True
        and cat["manufacturing_execution_intelligence_present_required"] is True
        and cat["factory_digital_twin_present_required"] is True
        and cat["industrial_knowledge_graph_present_required"] is True
        and cat["predictive_maintenance_present_required"] is True
        and cat["industrial_analytics_platform_present_required"] is True
        and cat["industrial_cybersecurity_present_required"] is True
        and cat["industry_40_50_alignment_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 11
        and cat["events"]["core_event_count"] == 8
        and cat["domain_model"]["entity_count"] == 12
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_e_physical_ai"] is True
        and cat["never_direct_ot_protocol_bypass"] is True
        and cat["ot_via_integration_platform_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_g"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        SmartFactoryRoot.enable(tenant_id="t1", factory_ref="f1").is_missing() is False,
        IndustrialAutomationRoot.enable(tenant_id="t1", automation_ref="a1").is_missing() is False,
        AutonomousManufacturingRoot.enable(tenant_id="t1", autonomous_ref="am1").is_missing() is False,
        ManufacturingExecutionRoot.enable(tenant_id="t1", mes_ref="m1").is_missing() is False,
        FactoryDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        PredictiveMaintenanceRoot.enable(tenant_id="t1", maintenance_ref="pm1").is_missing() is False,
        IndustrialKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        IndustrialCybersecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        IndustrialAnalyticsRoot.enable(tenant_id="t1", analytics_ref="an1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_industrial_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_e_physical_ai",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "ot_via_integration_platform_only", "never_direct_ot_protocol_bypass",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_industrial_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/industrial")', "/industrial/vision", "/industrial/domain",
        "/industrial/bounded-contexts", "/industrial/smart-factory", "/industrial/autonomous",
        "/industrial/automation", "/industrial/ai", "/industrial/digital-twin",
        "/industrial/knowledge-graph", "/industrial/maintenance", "/industrial/security",
        "/industrial/cqrs", "/industrial/events", "/industrial/microservices",
        "/industrial/integration", "/industrial/deployment", "/industrial/testing",
        "/industrial/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_INDUSTRIAL.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Smart Factory Platform is missing",
        "Never Industrial Automation Platform is missing",
        "Never Autonomous Manufacturing Platform is missing",
        "Never Manufacturing Execution Intelligence is missing",
        "Never Factory Digital Twin is missing",
        "Never Industrial Knowledge Graph is missing",
        "Never Predictive Maintenance is missing",
        "Never Industrial Analytics Platform is missing",
        "Never Industrial Cybersecurity is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Industry 4.0 / 5.0 Alignment is missing",
        "Never Cloud-Edge Industrial Deployment is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-E Physical AI",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Direct OT Protocol Bypass of Integration Platform",
        "Never Module-Local LLM",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "MEOS Smart Factory Platform SHALL integrate",
        "P216", "P216-E", "P215-Z", "P214-Z", "P216-G",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-F", "adr": 478, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
