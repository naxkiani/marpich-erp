"""Enterprise Regulatory Reporting Platform engine."""
from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime

from contexts.regulatory_reporting.domain.aggregates.regulatory_reporting_platform import (
    ExportFormat,
    RegulatorType,
    RegulatoryCapability,
    ReportCategory,
    SubmissionStatus,
)

PLATFORM_CATALOG: dict[str, dict] = {
    RegulatoryCapability.CENTRAL_BANK.value: {
        "label": "Central Bank",
        "regulator_type": RegulatorType.CENTRAL_BANK.value,
    },
    RegulatoryCapability.TAX_AUTHORITY.value: {
        "label": "Tax Authority",
        "regulator_type": RegulatorType.TAX_AUTHORITY.value,
        "delegates_to": "tax",
    },
    RegulatoryCapability.FINANCIAL_INTELLIGENCE_UNIT.value: {
        "label": "Financial Intelligence Unit",
        "regulator_type": RegulatorType.FINANCIAL_INTELLIGENCE_UNIT.value,
        "delegates_to": "aml",
    },
    RegulatoryCapability.AUDIT_AUTHORITY.value: {
        "label": "Audit Authority",
        "regulator_type": RegulatorType.AUDIT_AUTHORITY.value,
        "delegates_to": "audit",
    },
    RegulatoryCapability.GOVERNMENT.value: {
        "label": "Government",
        "regulator_type": RegulatorType.GOVERNMENT.value,
    },
    RegulatoryCapability.NGO_REPORTING.value: {
        "label": "NGO Reporting",
        "regulator_type": RegulatorType.NGO.value,
    },
    RegulatoryCapability.COMPLIANCE_REPORTS.value: {
        "label": "Compliance Reports",
        "category": ReportCategory.COMPLIANCE.value,
        "delegates_to": "compliance",
        "no_duplication": True,
    },
    RegulatoryCapability.RISK_REPORTS.value: {
        "label": "Risk Reports",
        "category": ReportCategory.RISK.value,
        "delegates_to": "risk",
        "no_duplication": True,
    },
    RegulatoryCapability.AML_REPORTS.value: {
        "label": "AML Reports",
        "category": ReportCategory.AML.value,
        "delegates_to": "currency_exchange.aml",
        "no_duplication": True,
    },
    RegulatoryCapability.KYC_REPORTS.value: {
        "label": "KYC Reports",
        "category": ReportCategory.KYC.value,
        "delegates_to": "banking.kyc",
        "no_duplication": True,
    },
    RegulatoryCapability.DIGITAL_SUBMISSION.value: {
        "label": "Digital Submission",
        "portal_integration": True,
    },
    RegulatoryCapability.XML_EXPORT.value: {
        "label": "XML",
        "format": ExportFormat.XML.value,
        "delegates_to": "reporting_engine",
    },
    RegulatoryCapability.JSON_EXPORT.value: {
        "label": "JSON",
        "format": ExportFormat.JSON.value,
        "delegates_to": "reporting_engine",
    },
    RegulatoryCapability.PDF_EXPORT.value: {
        "label": "PDF",
        "format": ExportFormat.PDF.value,
        "delegates_to": "reporting_engine",
    },
    RegulatoryCapability.COUNTRY_ADAPTERS.value: {
        "label": "Country Adapters",
        "configurable": True,
        "manifest_driven": True,
    },
    RegulatoryCapability.REGULATORY_DASHBOARD.value: {"label": "Regulatory Dashboard"},
}

POLICY_KEYS = [
    "regulatory_reporting.default_format",
    "regulatory_reporting.package.required",
    "regulatory_reporting.submission.audit",
    "regulatory_reporting.digital_submission.enabled",
    "regulatory_reporting.country.default",
]

REGULATOR_DELEGATION: dict[str, str | None] = {
    RegulatorType.TAX_AUTHORITY.value: "tax",
    RegulatorType.FINANCIAL_INTELLIGENCE_UNIT.value: "aml",
    RegulatorType.AUDIT_AUTHORITY.value: "audit",
    RegulatorType.CENTRAL_BANK.value: "treasury",
}

CATEGORY_DELEGATION: dict[str, str | None] = {
    ReportCategory.COMPLIANCE.value: "compliance",
    ReportCategory.RISK.value: "risk",
    ReportCategory.AML.value: "currency_exchange.aml",
    ReportCategory.KYC.value: "banking.kyc",
}

DEFAULT_COUNTRY_ADAPTERS: list[dict] = [
    {
        "country_code": "EXAMPLE",
        "country_name": "Example Republic",
        "regulator_types": ["tax_authority", "government", "compliance"],
        "supported_formats": ["xml", "json", "pdf"],
        "package_plugin_id": "regulatory-example",
        "portal_url": "https://portal.example.gov/submit",
    },
    {
        "country_code": "IR",
        "country_name": "Iran",
        "regulator_types": ["central_bank", "tax_authority", "financial_intelligence_unit"],
        "supported_formats": ["xml", "json", "pdf"],
        "package_plugin_id": "regulatory-banking-oecd",
        "portal_url": "https://cbi.ir/regulatory",
    },
    {
        "country_code": "US",
        "country_name": "United States",
        "regulator_types": ["government", "audit_authority", "financial_intelligence_unit"],
        "supported_formats": ["xml", "json", "pdf"],
        "package_plugin_id": "regulatory-banking-oecd",
        "portal_url": "https://www.fincen.gov/reporting",
    },
    {
        "country_code": "GLOBAL",
        "country_name": "Global / NGO",
        "regulator_types": ["ngo", "government", "compliance"],
        "supported_formats": ["xml", "json", "pdf"],
        "package_plugin_id": "regulatory-ngo-grants",
        "portal_url": "https://ngo-reporting.global/submit",
    },
]

REPORT_TYPE_MAP: dict[str, str] = {
    RegulatorType.CENTRAL_BANK.value: "central_bank",
    RegulatorType.TAX_AUTHORITY.value: "tax_authority",
    RegulatorType.FINANCIAL_INTELLIGENCE_UNIT.value: "financial_institution",
    RegulatorType.AUDIT_AUTHORITY.value: "audit",
    RegulatorType.GOVERNMENT.value: "government",
    RegulatorType.NGO.value: "ngo",
    ReportCategory.COMPLIANCE.value: "compliance",
    ReportCategory.RISK.value: "compliance",
    ReportCategory.AML.value: "financial_institution",
    ReportCategory.KYC.value: "financial_institution",
}


def list_capability_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in PLATFORM_CATALOG.items()]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def list_regulators() -> list[dict]:
    return [
        {
            "regulator_type": r.value,
            "label": r.value.replace("_", " ").title(),
            "delegates_to": REGULATOR_DELEGATION.get(r.value),
        }
        for r in RegulatorType
    ]


def list_report_categories() -> list[dict]:
    return [
        {
            "category": c.value,
            "label": c.value.replace("_", " ").title() + " Reports",
            "delegates_to": CATEGORY_DELEGATION.get(c.value),
        }
        for c in ReportCategory
    ]


def list_export_formats() -> list[dict]:
    return [
        {"format": f.value, "label": f.value.upper(), "delegates_to": "reporting_engine"}
        for f in ExportFormat
    ]


def dependency_map() -> dict:
    nodes = [{"id": "regulatory_reporting", "type": "platform", "label": "Enterprise Regulatory Reporting"}]
    edges = []
    for mod in ("reporting", "tax", "compliance", "risk", "currency_exchange", "banking", "audit", "grc"):
        nodes.append({"id": mod, "type": "module", "label": mod})
        edges.append({"from": mod, "to": "regulatory_reporting", "type": "feeds_reporting"})
    nodes.append({"id": "policy", "type": "shared_service", "label": "policy"})
    edges.append({"from": "regulatory_reporting", "to": "policy", "type": "delegates"})
    return {
        "nodes": nodes,
        "edges": edges,
        "hardcoded_regulatory_formats": False,
        "manifest_driven": True,
        "no_format_duplication": True,
    }


def resolve_report_type(*, regulator_type: str = "", report_category: str = "") -> str:
    if report_category and report_category in REPORT_TYPE_MAP:
        return REPORT_TYPE_MAP[report_category]
    return REPORT_TYPE_MAP.get(regulator_type, "compliance")


def find_adapter_for_country(adapters: list[dict], country_code: str) -> dict | None:
    code = country_code.upper()
    for adapter in adapters:
        if adapter.get("country_code", "").upper() == code and adapter.get("active", True):
            return adapter
    return None


def build_dashboard(
    *,
    profile: dict | None,
    adapters: list[dict],
    submissions: list[dict],
) -> dict:
    active_adapters = [a for a in adapters if a.get("active", True)]
    by_country: dict[str, int] = defaultdict(int)
    by_regulator: dict[str, int] = defaultdict(int)
    by_format: dict[str, int] = defaultdict(int)
    by_status: dict[str, int] = defaultdict(int)

    for sub in submissions:
        by_country[sub.get("country_code", "unknown")] += 1
        by_regulator[sub.get("regulator_type", "unknown")] += 1
        by_format[sub.get("export_format", "unknown")] += 1
        by_status[sub.get("status", "unknown")] += 1

    return {
        "summary": {
            "capabilities": len(PLATFORM_CATALOG),
            "country_adapters": len(active_adapters),
            "digital_submissions": len(submissions),
            "submitted_count": len([s for s in submissions if s.get("status") == SubmissionStatus.SUBMITTED.value]),
            "acknowledged_count": len([s for s in submissions if s.get("status") == SubmissionStatus.ACKNOWLEDGED.value]),
            "enabled_regulators": profile.get("enabled_regulators", []) if profile else [],
            "export_formats": [f.value for f in ExportFormat],
        },
        "by_country": dict(by_country),
        "by_regulator": dict(by_regulator),
        "by_format": dict(by_format),
        "by_status": dict(by_status),
        "adapters": active_adapters[:10],
        "recent_submissions": sorted(submissions, key=lambda s: s.get("created_at", ""), reverse=True)[:5],
        "delegation": {
            "reporting_engine_rendering": True,
            "manifest_driven_formats": True,
            "hardcoded_regulatory_formats": False,
            "local_format_duplication": False,
        },
        "generated_at": datetime.now(UTC).isoformat(),
    }
