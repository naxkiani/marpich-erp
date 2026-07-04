"""Default policy seeds per domain — activated on tenant provision."""
from __future__ import annotations

from datetime import UTC, datetime

DEFAULT_POLICY_TEMPLATES: dict[str, list[dict]] = {
    "hospital": [
        {
            "key": "admission.eligibility",
            "name": "Emergency Admission Criteria",
            "priority": 100,
            "conditions": [{"field": "encounter.type", "operator": "eq", "value": "emergency"}],
            "rules": [
                {
                    "outcome": "allow_admission",
                    "parameters": {"required_documents": ["id", "insurance_card"], "max_wait_minutes": 30},
                }
            ],
            "exceptions": [
                {
                    "id": "pediatric",
                    "name": "Pediatric override",
                    "conditions": [{"field": "patient.age", "operator": "lt", "value": 18}],
                    "rules": [
                        {
                            "outcome": "allow_admission",
                            "parameters": {"required_documents": ["guardian_consent"]},
                        }
                    ],
                }
            ],
            "approval_required": False,
        },
    ],
    "university": [
        {
            "key": "enrollment.max_credits",
            "name": "Maximum Credits Per Semester",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "within_limit", "parameters": {"max_credits": 24}}],
            "approval_required": False,
        },
    ],
    "bank": [
        {
            "key": "lending.single_exposure_limit",
            "name": "Single Exposure Limit",
            "priority": 100,
            "conditions": [{"field": "customer.tier", "operator": "eq", "value": "gold"}],
            "rules": [
                {"outcome": "within_limit", "parameters": {"max_amount": 750000, "requires_committee": False}}
            ],
            "approval_required": False,
        },
    ],
    "tax": [
        {
            "key": "vat.rate",
            "name": "Standard VAT Rate",
            "priority": 100,
            "conditions": [{"field": "jurisdiction", "operator": "eq", "value": "IR"}],
            "rules": [{"outcome": "apply_rate", "parameters": {"rate": 0.09}}],
            "exceptions": [
                {
                    "id": "medical_exempt",
                    "name": "Medical exemption",
                    "conditions": [{"field": "product.category", "operator": "eq", "value": "medical"}],
                    "rules": [{"outcome": "apply_rate", "parameters": {"rate": 0.0}}],
                }
            ],
            "approval_required": False,
        },
    ],
    "exchange": [
        {
            "key": "trading.hours",
            "name": "Regular Trading Hours",
            "priority": 100,
            "conditions": [],
            "rules": [
                {
                    "outcome": "market_open",
                    "parameters": {"open": "09:00", "close": "17:00", "timezone": "Asia/Tehran"},
                }
            ],
            "approval_required": False,
        },
    ],
    "construction": [
        {
            "key": "safety.ppe_required",
            "name": "PPE Requirement on Site",
            "priority": 100,
            "conditions": [{"field": "site.active", "operator": "eq", "value": True}],
            "rules": [{"outcome": "require_ppe", "parameters": {"items": ["helmet", "vest", "boots"]}}],
            "approval_required": False,
        },
    ],
    "government": [
        {
            "key": "procurement.threshold",
            "name": "Public Procurement Approval Threshold",
            "priority": 100,
            "conditions": [],
            "rules": [
                {
                    "outcome": "approval_required",
                    "parameters": {"threshold_amount": 50000, "currency": "USD"},
                }
            ],
            "approval_required": False,
        },
    ],
}


def default_effective_from() -> datetime:
    return datetime.now(UTC)
