"""P216-R Enterprise Financial Intelligence — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-R"
ADR = 490
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = (
    "Enterprise Robotics Financial Robotics, Autonomous Banking Operations, "
    "Intelligent Finance Automation & AI Financial Services Intelligence Platform"
)
CAPABILITY = "CAP-PLT-RB-001"
FINANCE_VISION = (
    "MEOS Financial Intelligence Platform SHALL unify financial robotics, "
    "autonomous banking operations, intelligent finance automation and finance digital twins as "
    "intelligent participants within the MEOS Financial Intelligence Ecosystem."
)
MISSION = (
    "Create an AI-native, secure, autonomous financial ecosystem "
    "that automates finance operations, improves decision-making, "
    "reduces operational risk and delivers intelligent financial services."
)
VISION = (
    "Every transaction, account, customer, financial asset, banking process, "
    "finance employee and regulatory workflow shall become an intelligent participant "
    "inside the MEOS Financial Intelligence Ecosystem."
)
FABRIC = "meos_financial_intelligence_fabric"
FOUNDATION_GATE = "P216"
MISSION_GATE = "P216-A"
STRATEGY_GATE = "P216-B"
DOMAIN_GATE = "P216-C"
RUNTIME_GATE = "P216-D"
PHYSICAL_AI_GATE = "P216-E"
INDUSTRIAL_GATE = "P216-F"
LOGISTICS_GATE = "P216-G"
MOBILITY_GATE = "P216-H"
HEALTHCARE_GATE = "P216-I"
CONSTRUCTION_GATE = "P216-K"
PUBLIC_SAFETY_GATE = "P216-L"
RETAIL_GATE = "P216-O"
HOSPITALITY_GATE = "P216-P"
EDUCATION_GATE = "P216-Q"
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_financial_intelligence"
AGGREGATE = "FinancialIntelligenceAggregate"

SUPPORTING_DOMAINS = (
    "banking_operations",
    "financial_transactions",
    "accounting_intelligence",
    "treasury_intelligence",
    "risk_management",
    "compliance_automation",
    "fraud_intelligence",
    "investment_intelligence",
    "payment_intelligence",
    "finance_robotics",
    "financial_analytics",
    "finance_digital_twin",
)
ENTITIES = (
    "FinancialInstitution",
    "BankAccount",
    "Customer",
    "Transaction",
    "Payment",
    "FinancialAsset",
    "Loan",
    "Investment",
    "RiskProfile",
    "ComplianceCase",
    "FinanceRobot",
    "FinancialAgent",
    "FinancialDigitalTwin",
)
VALUE_OBJECTS = (
    "TransactionAmount",
    "Currency",
    "RiskScore",
    "CreditScore",
    "ComplianceStatus",
    "AccountBalance",
    "FinancialPosition",
    "FraudProbability",
    "LiquidityScore",
    "AuditStatus",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Financial Transaction Context", "responsibilities": ("transaction_processing", "payment_intelligence", "settlement_management")},
    {"id": "BC-02", "name": "Banking Robotics Context", "responsibilities": ("financial_robots", "autonomous_banking_workflows", "robot_lifecycle")},
    {"id": "BC-03", "name": "Finance Automation Context", "responsibilities": ("accounting_automation", "reporting_automation", "financial_workflows")},
    {"id": "BC-04", "name": "Risk Intelligence Context", "responsibilities": ("risk_analysis", "fraud_detection", "predictive_risk_modelling")},
    {"id": "BC-05", "name": "Compliance Intelligence Context", "responsibilities": ("regulatory_monitoring", "compliance_automation", "audit_intelligence")},
    {"id": "BC-06", "name": "Investment Intelligence Context", "responsibilities": ("portfolio_intelligence", "market_analysis", "financial_optimisation")},
    {"id": "BC-07", "name": "Financial Digital Twin Context", "responsibilities": ("enterprise_financial_simulation", "scenario_modelling", "forecasting")},
    {"id": "BC-08", "name": "Financial Governance Context", "responsibilities": ("policy_management", "regulatory_governance", "financial_controls")},
)
FINANCIAL_ROBOTICS = {
    "present_required": True,
    "platform": "meos_financial_robotics_platform",
    "components": (
        "finance_robot_registry",
        "financial_agent_manager",
        "transaction_automation_engine",
        "accounting_robot_controller",
        "compliance_robot_engine",
        "finance_operations_dashboard",
    ),
    "supported_robotics": (
        "accounting_robots",
        "banking_service_robots",
        "customer_finance_assistants",
        "audit_robots",
        "compliance_monitoring_agents",
        "treasury_automation_agents",
    ),
    "capabilities": (
        "transaction_processing",
        "financial_reporting",
        "invoice_automation",
        "account_reconciliation",
        "audit_assistance",
        "compliance_monitoring",
    ),
}
AUTONOMOUS_BANKING = {
    "present_required": True,
    "platform": "meos_autonomous_banking_intelligence_platform",
    "capabilities": (
        "automated_banking_operations",
        "customer_service_automation",
        "digital_banking_assistance",
        "payment_intelligence",
        "account_intelligence",
        "credit_decision_support",
        "fraud_prevention",
    ),
    "models": (
        "banking_foundation_models",
        "financial_language_models",
        "risk_prediction_models",
        "fraud_detection_models",
        "customer_intelligence_models",
    ),
    "via_p214_z": True,
    "explainable_financial_ai": True,
    "regulatory_compliance_by_design": True,
}
FINANCE_AUTOMATION = {
    "present_required": True,
    "engine": "meos_finance_automation_engine",
    "capabilities": (
        "automated_accounting",
        "invoice_processing",
        "expense_management",
        "financial_reporting",
        "budget_intelligence",
        "forecast_automation",
        "tax_intelligence",
    ),
    "via_financial_kernel": True,
}
AI_FINANCE = {
    "present_required": True,
    "platform": "meos_ai_financial_intelligence_platform",
    "capabilities": (
        "financial_analysis",
        "autonomous_decision_support",
        "customer_intelligence",
        "forecasting",
    ),
    "via_p214_z": True,
    "explainable_financial_ai": True,
    "responsible_ai": True,
}
RISK_INTELLIGENCE = {
    "present_required": True,
    "engine": "meos_financial_risk_ai_engine",
    "capabilities": (
        "fraud_detection",
        "credit_risk_analysis",
        "market_risk_analysis",
        "operational_risk_prediction",
        "compliance_risk_analysis",
        "early_warning_intelligence",
    ),
    "via_p214_z": True,
}
COMPLIANCE_AUTOMATION = {
    "present_required": True,
    "platform": "meos_intelligent_compliance_platform",
    "capabilities": (
        "regulatory_monitoring",
        "compliance_automation",
        "audit_intelligence",
        "policy_enforcement",
    ),
    "via_policy_engine": True,
    "via_audit": True,
    "via_workflow": True,
}
FINANCE_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_finance_digital_twin_platform",
    "represents": (
        "banks", "enterprises", "accounts", "transactions", "assets",
        "liabilities", "cash_flow", "risk_profiles", "regulatory_environment",
    ),
    "capabilities": (
        "financial_simulation",
        "scenario_analysis",
        "forecasting",
        "risk_modelling",
        "liquidity_optimisation",
        "strategic_planning",
    ),
}
FINANCIAL_KG = {
    "present_required": True,
    "graph": "meos_financial_knowledge_graph",
    "nodes": (
        "customers", "accounts", "transactions", "assets", "banks",
        "regulations", "risks", "markets", "agents", "financial_robots",
    ),
    "relationships": (
        "owns", "transfers", "depends_on", "impacts",
        "controls", "complies_with", "optimises", "audits",
    ),
    "enables": (
        "financial_reasoning",
        "fraud_intelligence",
        "risk_analysis",
        "autonomous_decisions",
    ),
}
OBSERVABILITY = {
    "present_required": True,
    "platform": "meos_finance_observability_platform",
    "monitors": (
        "transaction_performance",
        "financial_robot_activity",
        "risk_levels",
        "fraud_indicators",
        "compliance_status",
        "ai_accuracy",
        "financial_kpis",
        "digital_twin_accuracy",
    ),
    "via_platform_observability": True,
}
SECURITY = {
    "present_required": True,
    "framework": "meos_financial_zero_trust_framework",
    "domains": (
        "customer_identity",
        "financial_identity",
        "transaction_security",
        "payment_security",
        "robot_identity",
        "ai_model_security",
        "regulatory_compliance",
        "audit_protection",
    ),
    "controls": (
        "multi_factor_authentication",
        "encryption",
        "fraud_detection",
        "continuous_monitoring",
        "financial_policy_enforcement",
        "ai_explainability",
    ),
    "zero_trust": True,
    "regulatory_compliance_by_design": True,
    "explainable_financial_ai": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration_platform": True,
    "via_financial_kernel": True,
    "payment_via_integration_platform_only": True,
    "never_direct_payment_bypass": True,
    "never_duplicate_core_banking_logic": True,
    "never_duplicate_accounting_gl_logic": True,
    "never_replace_financial_kernel": True,
    "no_module_local_llm": True,
    "physical_ai_via_p214z_acl_only": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_q_education": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
COMMANDS = (
    "CreateTransactionCommand",
    "ExecutePaymentCommand",
    "AssignFinanceRobotCommand",
    "RunRiskAnalysisCommand",
    "ApproveComplianceCommand",
    "UpdateFinanceTwinCommand",
)
QUERIES = (
    "GetAccountStatusQuery",
    "GetTransactionHistoryQuery",
    "GetRiskProfileQuery",
    "GetComplianceStatusQuery",
    "GetFinancialTwinQuery",
)
CORE_EVENTS = (
    {"name": "TransactionCreatedEvent", "schema": "robotics.finance.transaction.created.v1", "owner": "BC-01", "consumers": "risk,compliance,audit"},
    {"name": "PaymentCompletedEvent", "schema": "robotics.finance.payment.completed.v1", "owner": "BC-01", "consumers": "kernel,twin,audit"},
    {"name": "RiskDetectedEvent", "schema": "robotics.finance.risk.detected.v1", "owner": "BC-04", "consumers": "compliance,governance,audit"},
    {"name": "FraudAlertEvent", "schema": "robotics.finance.fraud.alert.v1", "owner": "BC-04", "consumers": "workflow,governance,audit"},
    {"name": "ComplianceValidatedEvent", "schema": "robotics.finance.compliance.validated.v1", "owner": "BC-05", "consumers": "transaction,audit"},
    {"name": "FinancialRobotCompletedEvent", "schema": "robotics.finance.robot.completed.v1", "owner": "BC-02", "consumers": "runtime,operations,audit"},
    {"name": "AuditGeneratedEvent", "schema": "robotics.finance.audit.generated.v1", "owner": "BC-05", "consumers": "governance,audit"},
    {"name": "FinancialOptimisedEvent", "schema": "robotics.finance.financial.optimised.v1", "owner": "BC-03", "consumers": "twin,analytics,audit"},
)
MICROSERVICES = (
    {"id": "transaction_intelligence_service", "bc": "BC-01", "api": "/robotics/finance/transactions", "db": "robotics_*", "events": ("TransactionCreatedEvent", "PaymentCompletedEvent"), "security": ("robotics.write",), "scaling": "transaction_replicas", "responsibility": "Transaction and payment projections"},
    {"id": "banking_robotics_service", "bc": "BC-02", "api": "/robotics/finance/robots", "db": "robotics_*", "events": ("FinancialRobotCompletedEvent",), "security": ("robotics.write",), "scaling": "robot_workers", "responsibility": "Financial robot mission orchestration"},
    {"id": "finance_automation_service", "bc": "BC-03", "api": "/robotics/finance/automation", "db": "robotics_*", "events": ("FinancialOptimisedEvent",), "security": ("robotics.write",), "scaling": "automation_workers", "responsibility": "Finance automation via Financial Kernel ACL"},
    {"id": "accounting_intelligence_service", "bc": "BC-03", "api": "/robotics/finance/accounting", "db": "robotics_*", "events": ("FinancialOptimisedEvent",), "security": ("robotics.write",), "scaling": "accounting_workers", "responsibility": "Accounting intelligence projections (no local GL)"},
    {"id": "risk_intelligence_service", "bc": "BC-04", "api": "/robotics/finance/risk", "db": "robotics_*", "events": ("RiskDetectedEvent", "FraudAlertEvent"), "security": ("robotics.write",), "scaling": "risk_workers", "responsibility": "Risk and fraud intelligence via P214-Z"},
    {"id": "compliance_service", "bc": "BC-05", "api": "/robotics/finance/compliance", "db": "robotics_*", "events": ("ComplianceValidatedEvent", "AuditGeneratedEvent"), "security": ("robotics.write",), "scaling": "compliance_workers", "responsibility": "Compliance automation facets"},
    {"id": "fraud_detection_service", "bc": "BC-04", "api": "/robotics/finance/fraud", "db": "robotics_*", "events": ("FraudAlertEvent",), "security": ("robotics.write",), "scaling": "fraud_workers", "responsibility": "Fraud detection projections"},
    {"id": "financial_digital_twin_service", "bc": "BC-07", "api": "/robotics/finance/digital-twin", "db": "robotics_*", "events": ("FinancialOptimisedEvent", "PaymentCompletedEvent"), "security": ("robotics.read",), "scaling": "twin_workers", "responsibility": "Finance digital twin sync"},
    {"id": "knowledge_graph_service", "bc": "BC-07", "api": "/robotics/finance/knowledge-graph", "db": "robotics_*", "events": ("TransactionCreatedEvent", "RiskDetectedEvent"), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Financial knowledge graph projections"},
    {"id": "finance_analytics_service", "bc": "BC-08", "api": "/robotics/finance/analytics", "db": "robotics_*", "events": ("FinancialOptimisedEvent", "AuditGeneratedEvent"), "security": ("robotics.read",), "scaling": "analytics_workers", "responsibility": "Finance analytics and governance facets"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p216d_robotics_os",
        "p216e_physical_ai",
        "p216g_autonomous_logistics",
        "p216q_education",
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "financial_kernel",
        "erp",
        "core_banking_systems",
        "payment_networks",
        "accounting_systems",
        "crm",
        "regulatory_platforms",
        "blockchain_platforms",
        "treasury_platforms",
        "integration_platform",
    ),
    "mechanisms": (
        "finance_apis",
        "robot_mission_interfaces",
        "payment_via_integration_connectors",
        "core_banking_via_peer_api",
        "gl_via_financial_kernel",
        "finance_event_contracts",
    ),
    "via_p216_d": True,
    "via_p216_e": True,
    "via_p216_g": True,
    "via_p216_q": True,
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p213": True,
    "via_financial_kernel": True,
    "via_integration_platform": True,
    "never_direct_payment_bypass": True,
    "never_duplicate_core_banking_logic": True,
    "never_duplicate_accounting_gl_logic": True,
    "never_replace_financial_kernel": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_financial_intelligence_infrastructure",
    "includes": (
        "financial_edge_platform",
        "banking_runtime_platform",
        "finance_cloud_platform",
        "ai_compute_cluster",
        "robot_control_platform",
        "digital_twin_cluster",
        "knowledge_graph_cluster",
        "analytics_platform",
        "security_operations_platform",
    ),
    "deployment_models": (
        "bank",
        "financial_enterprise",
        "fintech_ecosystem",
        "global_financial_network",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "transaction_testing",
    "payment_testing",
    "robot_workflow_testing",
    "financial_ai_validation",
    "risk_model_testing",
    "compliance_testing",
    "security_testing",
    "performance_testing",
    "resilience_testing",
    "regulatory_testing",
)
API_SURFACES = (
    "/api/v1/robotics/finance",
    "/api/v1/robotics/finance/vision",
    "/api/v1/robotics/finance/domain",
    "/api/v1/robotics/finance/bounded-contexts",
    "/api/v1/robotics/finance/robotics",
    "/api/v1/robotics/finance/autonomous-banking",
    "/api/v1/robotics/finance/automation",
    "/api/v1/robotics/finance/ai",
    "/api/v1/robotics/finance/risk",
    "/api/v1/robotics/finance/compliance",
    "/api/v1/robotics/finance/digital-twin",
    "/api/v1/robotics/finance/knowledge-graph",
    "/api/v1/robotics/finance/observability",
    "/api/v1/robotics/finance/security",
    "/api/v1/robotics/finance/cqrs",
    "/api/v1/robotics/finance/events",
    "/api/v1/robotics/finance/microservices",
    "/api/v1/robotics/finance/integration",
    "/api/v1/robotics/finance/deployment",
    "/api/v1/robotics/finance/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "financial_robotics_platform_is_missing",
    "autonomous_banking_platform_is_missing",
    "finance_automation_platform_is_missing",
    "ai_financial_intelligence_is_missing",
    "risk_intelligence_platform_is_missing",
    "financial_digital_twin_is_missing",
    "financial_knowledge_graph_is_missing",
    "compliance_automation_is_missing",
    "security_architecture_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_deployment_is_missing",
    "enterprise_finance_integration_is_missing",
    "testing_architecture_is_missing",
    "sibling_robotics_bc",
    "replace_p216_q_education",
    "replace_financial_kernel",
    "direct_payment_bypass",
    "duplicate_core_banking_logic",
    "duplicate_accounting_gl_logic",
    "module_local_llm",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Financial Intelligence Fabric",
        "finance_vision": FINANCE_VISION,
        "mission": MISSION,
        "vision": VISION,
        "builds_on_p216": True,
        "builds_on_p216_q": True,
        "builds_on_p216_g": True,
        "builds_on_p216_e": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "builds_on_financial_kernel": True,
        "never_replace_p216_q_education": True,
        "never_replace_financial_kernel": True,
        "foundation_gate": FOUNDATION_GATE,
        "education_gate": EDUCATION_GATE,
        "logistics_gate": LOGISTICS_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE,
        "runtime_gate": RUNTIME_GATE,
        "supreme_gate": SUPREME_GATE,
        "ai_gate": AI_GATE,
    }

def domain_model() -> dict[str, Any]:
    return {
        "present_required": True,
        "core_domain": CORE_DOMAIN,
        "aggregate": AGGREGATE,
        "supporting_domains": list(SUPPORTING_DOMAINS),
        "supporting_count": len(SUPPORTING_DOMAINS),
        "entities": list(ENTITIES),
        "entity_count": len(ENTITIES),
        "value_objects": list(VALUE_OBJECTS),
        "value_object_count": len(VALUE_OBJECTS),
    }

def bounded_contexts() -> dict[str, Any]:
    return {"present_required": True, "contexts": [dict(c) for c in BOUNDED_CONTEXTS], "context_count": len(BOUNDED_CONTEXTS)}

def robotics_platform() -> dict[str, Any]:
    return dict(FINANCIAL_ROBOTICS)

def autonomous_banking() -> dict[str, Any]:
    return dict(AUTONOMOUS_BANKING)

def finance_automation() -> dict[str, Any]:
    return dict(FINANCE_AUTOMATION)

def ai_finance() -> dict[str, Any]:
    return dict(AI_FINANCE)

def risk_intelligence() -> dict[str, Any]:
    return dict(RISK_INTELLIGENCE)

def compliance() -> dict[str, Any]:
    return dict(COMPLIANCE_AUTOMATION)

def digital_twin() -> dict[str, Any]:
    return dict(FINANCE_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(FINANCIAL_KG)

def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY)

def security() -> dict[str, Any]:
    return dict(SECURITY)

def cqrs() -> dict[str, Any]:
    return {"commands": list(COMMANDS), "command_count": len(COMMANDS), "queries": list(QUERIES), "query_count": len(QUERIES)}

def events() -> dict[str, Any]:
    return {"core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS)}

def microservices() -> dict[str, Any]:
    return {"services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def integration() -> dict[str, Any]:
    return dict(INTEGRATION)

def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)

def testing() -> dict[str, Any]:
    return {"present_required": True, "suites": list(TESTING), "suite_count": len(TESTING)}

def api() -> dict[str, Any]:
    return {
        "surfaces": list(API_SURFACES),
        "styles": list(API_STYLES),
        "api_first_present_required": True,
        "education_gate_api": "/api/v1/robotics/education",
        "runtime_gate_api": "/api/v1/robotics/runtime",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_s": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "finance_vision": FINANCE_VISION, "mission": MISSION, "vision": VISION, "principle": FINANCE_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE, "industrial_gate": INDUSTRIAL_GATE,
        "logistics_gate": LOGISTICS_GATE, "mobility_gate": MOBILITY_GATE,
        "healthcare_gate": HEALTHCARE_GATE, "construction_gate": CONSTRUCTION_GATE,
        "public_safety_gate": PUBLIC_SAFETY_GATE, "retail_gate": RETAIL_GATE,
        "hospitality_gate": HOSPITALITY_GATE, "education_gate": EDUCATION_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P216", "P216-A", "P216-B", "P216-C", "P216-D", "P216-E", "P216-F", "P216-G", "P216-H",
            "P216-I", "P216-K", "P216-L", "P216-O", "P216-P", "P216-Q", "P215-Z", "P214-Z", "P213",
            "Financial Kernel",
            "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476", "ADR-477", "ADR-478", "ADR-479",
            "ADR-480", "ADR-481", "ADR-483", "ADR-484", "ADR-487", "ADR-488", "ADR-489",
        ],
        "vision_pack": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "robotics_platform": robotics_platform(),
        "autonomous_banking": autonomous_banking(),
        "finance_automation": finance_automation(),
        "ai_finance": ai_finance(),
        "risk_intelligence": risk_intelligence(),
        "compliance": compliance(),
        "digital_twin": digital_twin(),
        "knowledge_graph": knowledge_graph(),
        "observability": observability(),
        "security": security(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "integration": integration(),
        "deployment": deployment(),
        "testing": testing(),
        "api": api(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "financial_robotics_platform_present_required": True,
        "autonomous_banking_platform_present_required": True,
        "finance_automation_platform_present_required": True,
        "ai_financial_intelligence_present_required": True,
        "risk_intelligence_platform_present_required": True,
        "financial_digital_twin_present_required": True,
        "financial_knowledge_graph_present_required": True,
        "compliance_automation_present_required": True,
        "security_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_deployment_present_required": True,
        "enterprise_finance_integration_present_required": True,
        "testing_architecture_present_required": True,
        "sibling_robotics_bc_forbidden": True,
        "never_replace_p216_foundation": True,
        "never_replace_p216_a_mission": True,
        "never_replace_p216_b_strategy": True,
        "never_replace_p216_c_domain": True,
        "never_replace_p216_d_runtime": True,
        "never_replace_p216_e_physical_ai": True,
        "never_replace_p216_f_industrial": True,
        "never_replace_p216_g_logistics": True,
        "never_replace_p216_h_mobility": True,
        "never_replace_p216_i_healthcare": True,
        "never_replace_p216_k_construction": True,
        "never_replace_p216_l_public_safety": True,
        "never_replace_p216_o_retail": True,
        "never_replace_p216_p_hospitality": True,
        "never_replace_p216_q_education": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_replace_financial_kernel": True,
        "never_direct_payment_bypass": True,
        "payment_via_integration_platform_only": True,
        "never_duplicate_core_banking_logic": True,
        "never_duplicate_accounting_gl_logic": True,
        "no_module_local_llm": True,
        "physical_ai_via_p214z_acl_only": True,
        "regulatory_compliance_by_design_required": True,
        "explainable_financial_ai_required": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_q": True, "builds_on_p216_g": True,
        "builds_on_p216_e": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True, "builds_on_financial_kernel": True,
        "via_p216_d": True, "via_p216_e": True, "via_p216_g": True, "via_p216_q": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_financial_kernel": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "via_integration_platform": True,
        "api_prefix": f"{API_PREFIX}/finance",
        "forbidden_sibling_bc": [
            "financial_robotics_platform",
            "autonomous_banking_platform",
            "ai_finance_operations_platform",
            "intelligent_accounting_automation_platform",
        ],
        "foundation_for_p216_s": True,
        "p216_j_agriculture_planned": True,
        "p216_m_space_planned": True,
        "p216_n_environmental_planned": True,
    }

def finance_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/finance",
        "GET /robotics/finance/vision",
        "GET /robotics/finance/domain",
        "GET /robotics/finance/bounded-contexts",
        "GET /robotics/finance/robotics",
        "GET /robotics/finance/autonomous-banking",
        "GET /robotics/finance/automation",
        "GET /robotics/finance/ai",
        "GET /robotics/finance/risk",
        "GET /robotics/finance/compliance",
        "GET /robotics/finance/digital-twin",
        "GET /robotics/finance/knowledge-graph",
        "GET /robotics/finance/observability",
        "GET /robotics/finance/security",
        "GET /robotics/finance/cqrs",
        "GET /robotics/finance/events",
        "GET /robotics/finance/microservices",
        "GET /robotics/finance/integration",
        "GET /robotics/finance/deployment",
        "GET /robotics/finance/testing",
        "GET /robotics/finance/readiness",
    ], "education_gate_routes": ["GET /robotics/education", "GET /robotics/education/readiness"]}
