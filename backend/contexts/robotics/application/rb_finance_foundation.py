"""Robotics P216-R financial robotics / autonomous banking foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/490-enterprise-robotics-finance.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_FINANCE.md",
    "docs/architecture/robotics/ROBOTICS_FINANCE_BANKING.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_FINANCE_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_FINANCE_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_FINANCE_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_FINANCE_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_finance.py",
    "backend/contexts/robotics/domain/aggregates/rb_finance_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_finance_acl.py",
    "backend/contexts/robotics/application/rb_finance_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/financial_robotics_platform",
    "backend/contexts/autonomous_banking_platform",
    "backend/contexts/ai_finance_operations_platform",
    "backend/contexts/intelligent_accounting_automation_platform",
)
def validate_rb_finance_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_finance_aggregates import (
        FinancialRoboticsRoot, AutonomousBankingRoot, FinanceAutomationRoot,
        AiFinancialIntelligenceRoot, RiskIntelligenceRoot, ComplianceAutomationRoot,
        FinancialDigitalTwinRoot, FinancialKnowledgeGraphRoot, FinanceSecurityRoot,
    )
    from contexts.robotics.domain.services import rb_platform_finance as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-R" and cat["adr"] == 490 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_financial_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["education_gate"] == "P216-Q"
        and cat["logistics_gate"] == "P216-G" and cat["physical_ai_gate"] == "P216-E"
        and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["financial_robotics_platform_present_required"] is True
        and cat["autonomous_banking_platform_present_required"] is True
        and cat["finance_automation_platform_present_required"] is True
        and cat["ai_financial_intelligence_present_required"] is True
        and cat["risk_intelligence_platform_present_required"] is True
        and cat["financial_digital_twin_present_required"] is True
        and cat["financial_knowledge_graph_present_required"] is True
        and cat["compliance_automation_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["domain_model"]["entity_count"] == 13
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_q_education"] is True
        and cat["never_replace_financial_kernel"] is True
        and cat["never_direct_payment_bypass"] is True
        and cat["never_duplicate_core_banking_logic"] is True
        and cat["never_duplicate_accounting_gl_logic"] is True
        and cat["no_module_local_llm"] is True
        and cat["regulatory_compliance_by_design_required"] is True
        and cat["explainable_financial_ai_required"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_s"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        FinancialRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        AutonomousBankingRoot.enable(tenant_id="t1", banking_ref="b1").is_missing() is False,
        FinanceAutomationRoot.enable(tenant_id="t1", automation_ref="a1").is_missing() is False,
        AiFinancialIntelligenceRoot.enable(tenant_id="t1", ai_ref="ai1").is_missing() is False,
        RiskIntelligenceRoot.enable(tenant_id="t1", risk_ref="rk1").is_missing() is False,
        ComplianceAutomationRoot.enable(tenant_id="t1", compliance_ref="c1").is_missing() is False,
        FinancialDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        FinancialKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        FinanceSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_finance_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i", "via_p216_k", "via_p216_l", "via_p216_o", "via_p216_p", "via_p216_q",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform", "via_financial_kernel",
        "via_core_banking_api", "via_payment_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_q_education",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_replace_financial_kernel",
        "never_direct_payment_bypass", "payment_via_integration_platform_only",
        "never_duplicate_core_banking_logic", "never_duplicate_accounting_gl_logic",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "regulatory_compliance_by_design_required", "explainable_financial_ai_required",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_finance_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/finance")', "/finance/vision", "/finance/domain",
        "/finance/bounded-contexts", "/finance/robotics", "/finance/autonomous-banking",
        "/finance/automation", "/finance/ai", "/finance/risk", "/finance/compliance",
        "/finance/digital-twin", "/finance/knowledge-graph", "/finance/observability",
        "/finance/security", "/finance/cqrs", "/finance/events", "/finance/microservices",
        "/finance/integration", "/finance/deployment", "/finance/testing",
        "/finance/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_FINANCE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Financial Robotics Platform is missing",
        "Never Autonomous Banking Platform is missing",
        "Never Finance Automation Platform is missing",
        "Never AI Financial Intelligence is missing",
        "Never Risk Intelligence Platform is missing",
        "Never Financial Digital Twin is missing",
        "Never Financial Knowledge Graph is missing",
        "Never Compliance Automation is missing",
        "Never Security Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Finance Integration is missing",
        "Never Testing Architecture is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-Q Education",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Financial Kernel",
        "Never Module-Local LLM",
        "Never Duplicate Core Banking Logic",
        "Never Duplicate Accounting GL Logic",
        "Never Direct Payment Bypass of Integration Platform",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Skip Regulatory Compliance by Design",
        "Never Skip Explainable Financial AI",
        "MEOS Financial Intelligence Platform SHALL unify",
        "P216", "P216-Q", "P215-Z", "P214-Z", "P216-S",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-R", "adr": 490, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
