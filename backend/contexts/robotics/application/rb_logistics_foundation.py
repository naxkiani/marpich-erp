"""Robotics P216-G autonomous logistics / warehouse foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/479-enterprise-robotics-logistics.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_LOGISTICS.md",
    "docs/architecture/robotics/ROBOTICS_LOGISTICS_WAREHOUSE.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_LOGISTICS_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_LOGISTICS_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_LOGISTICS_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_LOGISTICS_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_logistics.py",
    "backend/contexts/robotics/domain/aggregates/rb_logistics_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_logistics_acl.py",
    "backend/contexts/robotics/application/rb_logistics_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/autonomous_logistics_platform",
    "backend/contexts/warehouse_automation_platform",
    "backend/contexts/supply_chain_robotics_platform",
)
def validate_rb_logistics_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_logistics_aggregates import (
        AutonomousWarehouseRoot, SupplyChainRoboticsRoot, MaterialFlowRoot,
        WarehouseDigitalTwinRoot, AiLogisticsRoot, SupplyChainKnowledgeGraphRoot,
        TransportCoordinationRoot, WarehouseSecurityRoot, OrderFulfilmentRoot,
    )
    from contexts.robotics.domain.services import rb_platform_logistics as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-G" and cat["adr"] == 479 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_autonomous_logistics_fabric"
        and cat["foundation_gate"] == "P216" and cat["industrial_gate"] == "P216-F"
        and cat["physical_ai_gate"] == "P216-E" and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["autonomous_warehouse_platform_present_required"] is True
        and cat["supply_chain_robotics_platform_present_required"] is True
        and cat["intelligent_material_flow_platform_present_required"] is True
        and cat["warehouse_digital_twin_present_required"] is True
        and cat["ai_logistics_intelligence_present_required"] is True
        and cat["supply_chain_knowledge_graph_present_required"] is True
        and cat["transport_coordination_platform_present_required"] is True
        and cat["warehouse_security_architecture_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 11
        and cat["events"]["core_event_count"] == 9
        and cat["domain_model"]["entity_count"] == 15
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_f_industrial"] is True
        and cat["never_duplicate_wms_tms_core_logic"] is True
        and cat["no_module_local_llm"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_h"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        AutonomousWarehouseRoot.enable(tenant_id="t1", warehouse_ref="w1").is_missing() is False,
        SupplyChainRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        MaterialFlowRoot.enable(tenant_id="t1", flow_ref="f1").is_missing() is False,
        WarehouseDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        AiLogisticsRoot.enable(tenant_id="t1", ai_ref="a1").is_missing() is False,
        SupplyChainKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        TransportCoordinationRoot.enable(tenant_id="t1", transport_ref="t1").is_missing() is False,
        WarehouseSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        OrderFulfilmentRoot.enable(tenant_id="t1", fulfilment_ref="fu1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_logistics_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f",
        "via_p215_z", "via_p214_z", "via_p213", "via_wms_api", "via_tms_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_f_industrial",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_duplicate_wms_tms_core_logic", "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_logistics_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/logistics")', "/logistics/vision", "/logistics/domain",
        "/logistics/bounded-contexts", "/logistics/warehouse", "/logistics/robotics",
        "/logistics/material-flow", "/logistics/ai", "/logistics/digital-twin",
        "/logistics/knowledge-graph", "/logistics/transport", "/logistics/security",
        "/logistics/cqrs", "/logistics/events", "/logistics/microservices",
        "/logistics/integration", "/logistics/deployment", "/logistics/testing",
        "/logistics/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_LOGISTICS.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Autonomous Warehouse Platform is missing",
        "Never Supply Chain Robotics Platform is missing",
        "Never Intelligent Material Flow Platform is missing",
        "Never Warehouse Digital Twin is missing",
        "Never AI Logistics Intelligence is missing",
        "Never Supply Chain Knowledge Graph is missing",
        "Never Transport Coordination Platform is missing",
        "Never Warehouse Security Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Supply Chain Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-F Industrial",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Module-Local LLM",
        "Never Duplicate WMS/TMS Core Logic",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "MEOS Autonomous Logistics Platform SHALL unify",
        "P216", "P216-F", "P215-Z", "P214-Z", "P216-H",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-G", "adr": 479, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
