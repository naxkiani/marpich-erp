"""Default compliance controls seeded per industry pack."""
from __future__ import annotations

DEFAULT_CONTROLS: tuple[tuple[str, str, str, str], ...] = (
    ("internal_policies", "POL-001", "Required policies active", "high"),
    ("financial_compliance", "SOX-001", "Journal posting audit trail", "critical"),
    ("financial_compliance", "SOX-002", "Segregation of duties on finance actions", "critical"),
    ("tax_compliance", "TAX-001", "Tax rate policy evaluated before invoice", "high"),
    ("educational_compliance", "FERPA-001", "Student record access logged", "critical"),
    ("healthcare_compliance", "HIPAA-164.312-b", "PHI access audit with reason", "critical"),
    ("document_compliance", "DOC-001", "Regulated document download audited", "high"),
    ("security_compliance", "SEC-001", "Excessive failed login threshold", "high"),
    ("security_compliance", "SEC-002", "Access denial spike detection", "medium"),
    ("audit_compliance", "AUD-001", "Audit export integrity", "critical"),
    ("audit_compliance", "AUD-002", "Retention purge documented", "high"),
    ("data_privacy", "GDPR-001", "Erasure request SLA", "critical"),
    ("data_privacy", "GDPR-002", "Consent recorded before processing", "high"),
    ("retention_policies", "RET-001", "No purge under legal hold", "critical"),
    ("retention_policies", "RET-002", "Document retention schedule applied", "medium"),
)

INDUSTRY_PACK_DOMAINS: dict[str, tuple[str, ...]] = {
    "hospital": ("healthcare_compliance", "document_compliance", "security_compliance", "audit_compliance", "retention_policies", "data_privacy", "internal_policies"),
    "clinic": ("healthcare_compliance", "document_compliance", "security_compliance", "audit_compliance", "retention_policies"),
    "university": ("educational_compliance", "document_compliance", "security_compliance", "audit_compliance", "data_privacy", "internal_policies"),
    "school": ("educational_compliance", "document_compliance", "security_compliance", "audit_compliance"),
    "bank": ("financial_compliance", "security_compliance", "audit_compliance", "internal_policies", "retention_policies"),
    "tax_consulting": ("tax_compliance", "financial_compliance", "document_compliance", "audit_compliance", "internal_policies"),
    "government": ("internal_policies", "document_compliance", "security_compliance", "audit_compliance", "retention_policies", "data_privacy"),
    "municipality": ("internal_policies", "document_compliance", "security_compliance", "retention_policies"),
}

COMPLIANCE_DOMAINS: tuple[tuple[str, str], ...] = (
    ("internal_policies", "Internal Policies"),
    ("financial_compliance", "Financial Compliance"),
    ("tax_compliance", "Tax Compliance"),
    ("educational_compliance", "Educational Compliance"),
    ("healthcare_compliance", "Healthcare Compliance"),
    ("document_compliance", "Document Compliance"),
    ("security_compliance", "Security Compliance"),
    ("audit_compliance", "Audit Compliance"),
    ("data_privacy", "Data Privacy"),
    ("retention_policies", "Retention Policies"),
)
