"""Enterprise Regulatory Reporting Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class RegulatoryCapability(StrEnum):
    CENTRAL_BANK = "central_bank"
    TAX_AUTHORITY = "tax_authority"
    FINANCIAL_INTELLIGENCE_UNIT = "financial_intelligence_unit"
    AUDIT_AUTHORITY = "audit_authority"
    GOVERNMENT = "government"
    NGO_REPORTING = "ngo_reporting"
    COMPLIANCE_REPORTS = "compliance_reports"
    RISK_REPORTS = "risk_reports"
    AML_REPORTS = "aml_reports"
    KYC_REPORTS = "kyc_reports"
    DIGITAL_SUBMISSION = "digital_submission"
    XML_EXPORT = "xml_export"
    JSON_EXPORT = "json_export"
    PDF_EXPORT = "pdf_export"
    COUNTRY_ADAPTERS = "country_adapters"
    REGULATORY_DASHBOARD = "regulatory_dashboard"


class RegulatorType(StrEnum):
    CENTRAL_BANK = "central_bank"
    TAX_AUTHORITY = "tax_authority"
    FINANCIAL_INTELLIGENCE_UNIT = "financial_intelligence_unit"
    AUDIT_AUTHORITY = "audit_authority"
    GOVERNMENT = "government"
    NGO = "ngo"


class ReportCategory(StrEnum):
    COMPLIANCE = "compliance"
    RISK = "risk"
    AML = "aml"
    KYC = "kyc"


class ExportFormat(StrEnum):
    XML = "xml"
    JSON = "json"
    PDF = "pdf"


class SubmissionStatus(StrEnum):
    DRAFT = "draft"
    RENDERED = "rendered"
    SUBMITTED = "submitted"
    ACKNOWLEDGED = "acknowledged"
    REJECTED = "rejected"


@dataclass(eq=False, kw_only=True)
class RegulatoryTenantProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    default_format: str = "json"
    default_country: str = "EXAMPLE"
    digital_submission_enabled: bool = True
    enabled_regulators: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        profile_ref: str,
        enabled_regulators: list[str],
        metadata: dict | None = None,
    ) -> RegulatoryTenantProfile:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            profile_ref=profile_ref,
            enabled_regulators=enabled_regulators,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "default_format": self.default_format,
            "default_country": self.default_country,
            "digital_submission_enabled": self.digital_submission_enabled,
            "enabled_regulators": self.enabled_regulators,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class CountryAdapter(AggregateRoot):
    tenant_id: str
    adapter_ref: str
    country_code: str
    country_name: str
    regulator_types: list[str] = field(default_factory=list)
    supported_formats: list[str] = field(default_factory=list)
    package_plugin_id: str = ""
    portal_url: str = ""
    active: bool = True
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def configure(
        cls,
        *,
        tenant_id: str,
        adapter_ref: str,
        country_code: str,
        country_name: str,
        regulator_types: list[str],
        supported_formats: list[str],
        package_plugin_id: str = "",
        portal_url: str = "",
        metadata: dict | None = None,
    ) -> CountryAdapter:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            adapter_ref=adapter_ref,
            country_code=country_code.upper(),
            country_name=country_name,
            regulator_types=regulator_types,
            supported_formats=supported_formats,
            package_plugin_id=package_plugin_id,
            portal_url=portal_url,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "adapter_ref": self.adapter_ref,
            "tenant_id": self.tenant_id,
            "country_code": self.country_code,
            "country_name": self.country_name,
            "regulator_types": self.regulator_types,
            "supported_formats": self.supported_formats,
            "package_plugin_id": self.package_plugin_id,
            "portal_url": self.portal_url,
            "active": self.active,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class DigitalSubmission(AggregateRoot):
    tenant_id: str
    submission_ref: str
    adapter_ref: str
    country_code: str
    regulator_type: str
    report_category: str
    export_format: str
    status: str
    reporting_submission_ref: str = ""
    portal_reference: str = ""
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    submitted_at: str | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        submission_ref: str,
        adapter_ref: str,
        country_code: str,
        regulator_type: str,
        report_category: str,
        export_format: str,
        reporting_submission_ref: str = "",
        metadata: dict | None = None,
    ) -> DigitalSubmission:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            submission_ref=submission_ref,
            adapter_ref=adapter_ref,
            country_code=country_code,
            regulator_type=regulator_type,
            report_category=report_category,
            export_format=export_format,
            status=SubmissionStatus.DRAFT.value,
            reporting_submission_ref=reporting_submission_ref,
            metadata=metadata or {},
        )

    def mark_rendered(self, reporting_submission_ref: str) -> None:
        self.status = SubmissionStatus.RENDERED.value
        self.reporting_submission_ref = reporting_submission_ref

    def submit(self, portal_reference: str = "") -> None:
        self.status = SubmissionStatus.SUBMITTED.value
        self.portal_reference = portal_reference
        self.submitted_at = datetime.now(UTC).isoformat()

    def acknowledge(self) -> None:
        self.status = SubmissionStatus.ACKNOWLEDGED.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "submission_ref": self.submission_ref,
            "tenant_id": self.tenant_id,
            "adapter_ref": self.adapter_ref,
            "country_code": self.country_code,
            "regulator_type": self.regulator_type,
            "report_category": self.report_category,
            "export_format": self.export_format,
            "status": self.status,
            "reporting_submission_ref": self.reporting_submission_ref,
            "portal_reference": self.portal_reference,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "submitted_at": self.submitted_at,
        }
