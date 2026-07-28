"""P213-P Enterprise Testing, Governance, Compliance Validation & Definition of Done Platform — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P213-P"
ADR = 420
SOR = "analytics"
API_PREFIX = "/api/v1/analytics"
PRODUCT = "Enterprise BI Testing, Governance, Compliance Validation & DoD Platform"
CAPABILITY = "CAP-PLT-BI-001"
PRINCIPLE = "BI systems SHALL prove correctness, security, compliance, and governance continuously."

CAPABILITIES = (
    "testing_framework",
    "governance_validation",
    "compliance_automation",
    "definition_of_done",
    "certification",
)
DOMAIN_EVENTS = (
    "BiValidationStarted",
    "BiCompliancePassed",
    "BiEvidenceGenerated",
    "BiCertificationIssued",
)
CURSOR_OUTPUTS = (
    "architecture_vision",
    "domain_model",
    "capabilities",
    "cqrs",
    "events",
    "apis",
    "security",
    "integrations",
    "production_readiness_checklist",
)
QUALITY_GATES_REJECT_IF = (
    "bi_assurance_architecture_is_incomplete",
    "sibling_business_intelligence_bc",
)


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "adr": ADR,
        "sor": SOR,
        "product": PRODUCT,
        "capability": CAPABILITY,
        "principle": PRINCIPLE,
        "builds_on": [
            "P213-A",
            "P213-O",
            "ADR-394",
            "ADR-419",
        ],
        "architecture": {
            "present_required": True,
            "not_incomplete": True,
            "capabilities": list(CAPABILITIES),
            "capability_count": len(CAPABILITIES),
        },
        "cqrs": {
            "events": list(DOMAIN_EVENTS),
            "event_count": len(DOMAIN_EVENTS),
        },
        "cursor_outputs": {"outputs": list(CURSOR_OUTPUTS), "count": len(CURSOR_OUTPUTS)},
        "quality_gates": {"reject_if": list(QUALITY_GATES_REJECT_IF)},
        "production_readiness": {"verdict": "ENTERPRISE_GRADE", "prompt_id": PROMPT_ID},
        "architecture_present_required": True,
        "sibling_business_intelligence_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/qa",
        "forbidden_sibling_bc": [
            "business_intelligence",
            "decision_intelligence",
            "reporting_platform",
            "metric_governance_platform",
            "visualization_platform",
            "bi_core",
        ],
    }


def qa_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /analytics/qa",
            "GET /analytics/qa/readiness",
        ],
    }


def production_readiness() -> dict[str, Any]:
    return catalog()["production_readiness"]
