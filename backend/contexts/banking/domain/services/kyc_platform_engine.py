"""Enterprise KYC Platform engine."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.banking.domain.aggregates.kyc_platform_engine import (
    DocumentType,
    DueDiligenceLevel,
    KYC_CASE_TRANSITIONS,
    KycCaseStatus,
    PepStatus,
    ReviewStatus,
    RiskClass,
    SanctionsStatus,
)

KYC_PLATFORM_CATALOG: dict[str, dict] = {
    "identity_verification": {"label": "Identity Verification", "supported": True},
    DocumentType.PASSPORT.value: {"label": "Passport", "document_type": True},
    DocumentType.NATIONAL_ID.value: {"label": "National ID", "document_type": True},
    DocumentType.BUSINESS_REGISTRATION.value: {"label": "Business Registration", "document_type": True},
    DocumentType.TAX_NUMBER.value: {"label": "Tax Number", "document_type": True},
    "address_verification": {"label": "Address Verification", "supported": True},
    "risk_classification": {"label": "Risk Classification", "supported": True},
    DueDiligenceLevel.STANDARD.value: {"label": "Customer Due Diligence", "cdd": True},
    DueDiligenceLevel.ENHANCED.value: {"label": "Enhanced Due Diligence", "edd": True},
    "pep_flag": {"label": "PEP Flag", "screening_type": "pep"},
    "sanctions_screening": {"label": "Sanctions Screening Hook", "screening_type": "sanctions"},
    "document_verification": {"label": "Document Verification", "supported": True},
    "biometric_extension": {"label": "Biometric Extension Hook", "hook": True},
    "workflow_approval": {"label": "Workflow Approval", "supported": True},
    "periodic_review": {"label": "Periodic Review", "supported": True},
    "audit_trail": {"label": "Audit Trail", "supported": True},
    "policy_engine_rules": {"label": "Configurable KYC Rules", "policy_domain": "bank"},
}

KYC_POLICY_KEYS: list[dict] = [
    {
        "key": "kyc.identity.verification_required",
        "description": "Required identity documents by customer segment",
        "facts": ["customer_type", "segment", "document_types"],
    },
    {
        "key": "kyc.document.passport_validity",
        "description": "Minimum passport validity in days",
        "facts": ["document_type", "expiry_date", "days_until_expiry"],
    },
    {
        "key": "kyc.risk.classification",
        "description": "Risk class assignment rules",
        "facts": ["customer_type", "country", "pep_status", "transaction_volume"],
    },
    {
        "key": "kyc.dd.enhanced_threshold",
        "description": "Conditions triggering Enhanced Due Diligence",
        "facts": ["risk_class", "pep_status", "amount", "country_risk"],
    },
    {
        "key": "kyc.pep.screening",
        "description": "PEP screening outcome rules",
        "facts": ["match_score", "customer_type", "role"],
    },
    {
        "key": "kyc.sanctions.screening",
        "description": "Sanctions screening outcome rules",
        "facts": ["match_score", "list_name", "country"],
    },
    {
        "key": "kyc.periodic.review_interval",
        "description": "Periodic KYC review interval by risk class",
        "facts": ["risk_class", "due_diligence_level"],
    },
    {
        "key": "kyc.approval.required_level",
        "description": "Approval levels required for KYC case completion",
        "facts": ["risk_class", "due_diligence_level", "pep_status"],
    },
]


def list_kyc_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in KYC_PLATFORM_CATALOG.items()]


def list_kyc_policy_keys() -> list[dict]:
    return KYC_POLICY_KEYS


def list_case_workflow() -> list[dict]:
    return [
        {"status": status, "allowed_transitions": transitions}
        for status, transitions in KYC_CASE_TRANSITIONS.items()
    ]


def classify_risk_from_policy(*, policy_outcome: str | None, policy_params: dict) -> tuple[str, bool]:
    risk = policy_params.get("risk_class", RiskClass.LOW.value)
    requires_edd = policy_params.get("requires_edd", False)
    if policy_outcome == "enhanced_due_diligence":
        return RiskClass.HIGH.value, True
    if policy_outcome in {"high_risk", "confirmed_pep"}:
        return RiskClass.HIGH.value, bool(requires_edd or True)
    if policy_outcome == "medium_risk":
        return RiskClass.MEDIUM.value, bool(requires_edd)
    if policy_outcome == "low_risk":
        return RiskClass.LOW.value, bool(requires_edd)
    return risk, bool(requires_edd)


def resolve_pep_status_from_policy(*, policy_outcome: str | None, match_score: float) -> str:
    if policy_outcome == "confirmed_pep":
        return PepStatus.CONFIRMED.value
    if policy_outcome in {"potential_match", "review_required"} or match_score >= 0.7:
        return PepStatus.POTENTIAL_MATCH.value
    return PepStatus.CLEAR.value


def resolve_sanctions_status_from_policy(*, policy_outcome: str | None, match_score: float) -> str:
    if policy_outcome == "block":
        return SanctionsStatus.BLOCKED.value
    if policy_outcome in {"potential_match", "review_required"} or match_score >= 0.8:
        return SanctionsStatus.POTENTIAL_MATCH.value
    return SanctionsStatus.CLEAR.value


def resolve_approval_levels(*, risk_class: str, requires_edd: bool, pep_status: str) -> int:
    if pep_status == PepStatus.CONFIRMED.value or risk_class == RiskClass.CRITICAL.value:
        return 3
    if requires_edd or risk_class == RiskClass.HIGH.value:
        return 2
    if risk_class == RiskClass.MEDIUM.value:
        return 1
    return 1


def build_kyc_dashboard(
    *,
    cases: list[dict],
    documents: list[dict],
    reviews: list[dict],
    screenings: list[dict],
) -> dict:
    by_status: dict[str, int] = {}
    by_risk: dict[str, int] = {}
    by_ddl: dict[str, int] = {}
    pep_flags = 0
    sanctions_hits = 0
    overdue_reviews = 0

    for c in cases:
        by_status[c.get("status", "unknown")] = by_status.get(c.get("status", "unknown"), 0) + 1
        by_risk[c.get("risk_class", "unknown")] = by_risk.get(c.get("risk_class", "unknown"), 0) + 1
        by_ddl[c.get("due_diligence_level", "unknown")] = (
            by_ddl.get(c.get("due_diligence_level", "unknown"), 0) + 1
        )
        if c.get("pep_status") in {PepStatus.POTENTIAL_MATCH.value, PepStatus.CONFIRMED.value}:
            pep_flags += 1
        if c.get("sanctions_status") in {
            SanctionsStatus.POTENTIAL_MATCH.value,
            SanctionsStatus.BLOCKED.value,
        }:
            sanctions_hits += 1

    verified_docs = sum(1 for d in documents if d.get("verification_status") == "verified")
    for r in reviews:
        if r.get("status") == ReviewStatus.OVERDUE.value:
            overdue_reviews += 1

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "summary": {
            "case_count": len(cases),
            "pending_approval": by_status.get(KycCaseStatus.PENDING_APPROVAL.value, 0),
            "approved_cases": by_status.get(KycCaseStatus.APPROVED.value, 0),
            "document_count": len(documents),
            "verified_documents": verified_docs,
            "screening_count": len(screenings),
            "pep_flags": pep_flags,
            "sanctions_hits": sanctions_hits,
            "overdue_reviews": overdue_reviews,
            "review_count": len(reviews),
        },
        "by_case_status": by_status,
        "by_risk_class": by_risk,
        "by_due_diligence_level": by_ddl,
        "case_workflow": list_case_workflow(),
        "policy_keys": list_kyc_policy_keys(),
    }
