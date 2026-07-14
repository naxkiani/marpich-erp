"""Privacy & compliance controls for federation identity data (P198-C2)."""
from __future__ import annotations

COMPLIANCE_FRAMEWORKS = (
    "ISO_27001",
    "ISO_27701",
    "SOC_2",
    "PCI_DSS",
    "GDPR",
    "HIPAA",
    "NIST_CSF",
    "OWASP_ASVS",
    "OpenID_Foundation",
)


def privacy_controls() -> dict:
    return {
        "frameworks": list(COMPLIANCE_FRAMEWORKS),
        "data_minimization": True,
        "purpose_limitation": True,
        "consent_required_for_marketing": True,
        "pii_in_logs": False,
        "encryption_at_rest": "AES-256",
        "encryption_in_transit": "TLS_1_2+",
    }


def retention_policies() -> list[dict]:
    return [
        {"data_class": "federation_audit", "retention_days": 2555, "legal_hold_capable": True},
        {"data_class": "federation_sessions", "retention_days": 90, "legal_hold_capable": False},
        {"data_class": "ai_predictions", "retention_days": 365, "legal_hold_capable": True},
        {"data_class": "consent_records", "retention_days": 2555, "legal_hold_capable": True},
        {"data_class": "feature_store", "retention_days": 180, "legal_hold_capable": False},
    ]


def privacy_impact_assessment() -> dict:
    return {
        "assessment": "federation_ai_pia_v1",
        "status": "approved_template",
        "risks": [
            {"risk": "automated_decision_impact", "mitigation": "explainability_required + human_review_on_deny"},
            {"risk": "cross_border_identity", "mitigation": "tenant_region_policy + data_residency"},
            {"risk": "training_data_leakage", "mitigation": "tenant_isolated_features + no_raw_pii_in_models"},
        ],
        "dpia_required": True,
    }


def consent_record(*, subject_id: str, purpose: str, granted: bool) -> dict:
    from datetime import UTC, datetime

    return {
        "subject_id": subject_id,
        "purpose": purpose,
        "granted": granted,
        "recorded_at": datetime.now(UTC).isoformat(),
        "lawful_basis": "consent" if granted else "withdrawn",
    }


def audit_export_manifest(*, tenant_id: str, from_date: str | None = None, to_date: str | None = None) -> dict:
    return {
        "tenant_id": tenant_id,
        "from_date": from_date,
        "to_date": to_date,
        "formats": ["json", "csv"],
        "includes": ["federation_events", "trust_decisions", "ai_predictions", "policy_decisions"],
        "redaction": "pii_minimized",
    }
