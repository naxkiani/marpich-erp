"""Robotics P216-O retail / autonomous commerce foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/487-enterprise-robotics-retail.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_RETAIL.md",
    "docs/architecture/robotics/ROBOTICS_RETAIL_STORE.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_RETAIL_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_RETAIL_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_RETAIL_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_RETAIL_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_retail.py",
    "backend/contexts/robotics/domain/aggregates/rb_retail_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_retail_acl.py",
    "backend/contexts/robotics/application/rb_retail_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/retail_robotics_platform",
    "backend/contexts/autonomous_commerce_platform",
    "backend/contexts/customer_experience_automation_platform",
    "backend/contexts/smart_store_automation_platform",
)
def validate_rb_retail_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_retail_aggregates import (
        RetailRoboticsRoot, CustomerExperienceRoot, AutonomousCommerceRoot,
        SmartStoreRoot, CommerceAiRoot, RetailDigitalTwinRoot,
        CommerceKnowledgeGraphRoot, RetailSecurityRoot, InventoryIntelligenceRoot,
    )
    from contexts.robotics.domain.services import rb_platform_retail as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-O" and cat["adr"] == 487 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_autonomous_commerce_fabric"
        and cat["foundation_gate"] == "P216" and cat["public_safety_gate"] == "P216-L"
        and cat["logistics_gate"] == "P216-G" and cat["physical_ai_gate"] == "P216-E"
        and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["retail_robotics_platform_present_required"] is True
        and cat["customer_experience_automation_present_required"] is True
        and cat["autonomous_commerce_platform_present_required"] is True
        and cat["smart_store_platform_present_required"] is True
        and cat["commerce_ai_platform_present_required"] is True
        and cat["retail_digital_twin_present_required"] is True
        and cat["commerce_knowledge_graph_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["domain_model"]["entity_count"] == 13
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_l_public_safety"] is True
        and cat["never_direct_payment_bypass"] is True
        and cat["never_duplicate_pos_sales_crm_core_logic"] is True
        and cat["no_module_local_llm"] is True
        and cat["privacy_by_design_required"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_p"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        RetailRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        CustomerExperienceRoot.enable(tenant_id="t1", experience_ref="e1").is_missing() is False,
        AutonomousCommerceRoot.enable(tenant_id="t1", commerce_ref="c1").is_missing() is False,
        SmartStoreRoot.enable(tenant_id="t1", store_ref="s1").is_missing() is False,
        CommerceAiRoot.enable(tenant_id="t1", ai_ref="a1").is_missing() is False,
        RetailDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        CommerceKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        RetailSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        InventoryIntelligenceRoot.enable(tenant_id="t1", inventory_ref="i1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_retail_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i", "via_p216_k", "via_p216_l",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_pos_api", "via_crm_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_l_public_safety",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_direct_payment_bypass", "payment_via_integration_platform_only",
        "never_duplicate_pos_sales_crm_core_logic",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only", "privacy_by_design_required",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_retail_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/retail")', "/retail/vision", "/retail/domain",
        "/retail/bounded-contexts", "/retail/robotics", "/retail/customer-experience",
        "/retail/commerce", "/retail/smart-store", "/retail/commerce-ai",
        "/retail/digital-twin", "/retail/knowledge-graph", "/retail/observability",
        "/retail/security", "/retail/cqrs", "/retail/events", "/retail/microservices",
        "/retail/integration", "/retail/deployment", "/retail/testing",
        "/retail/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_RETAIL.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Retail Robotics Platform is missing",
        "Never Customer Experience Automation is missing",
        "Never Autonomous Commerce Platform is missing",
        "Never Smart Store Platform is missing",
        "Never Commerce AI Platform is missing",
        "Never Retail Digital Twin is missing",
        "Never Commerce Knowledge Graph is missing",
        "Never Security Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Retail Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-L Public Safety",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Module-Local LLM",
        "Never Duplicate POS/Sales/CRM Core Logic",
        "Never Direct Payment Bypass of Integration Platform",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Skip Privacy by Design for Customer Data",
        "MEOS Autonomous Commerce Platform SHALL unify",
        "P216", "P216-L", "P215-Z", "P214-Z", "P216-P",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-O", "adr": 487, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
