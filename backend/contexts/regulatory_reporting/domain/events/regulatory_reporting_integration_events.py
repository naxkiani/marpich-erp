"""Enterprise Regulatory Reporting Platform integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class CountryAdapterConfiguredIntegration(IntegrationEvent):
    adapter_ref: str
    country_code: str

    @property
    def event_name(self) -> str:
        return "regulatory.adapter.configured"

    @property
    def source_context(self) -> str:
        return "regulatory_reporting"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"adapter_ref": self.adapter_ref, "country_code": self.country_code}


@dataclass(frozen=True, kw_only=True)
class DigitalSubmissionCreatedIntegration(IntegrationEvent):
    submission_ref: str
    country_code: str
    regulator_type: str
    export_format: str

    @property
    def event_name(self) -> str:
        return "regulatory.submission.created"

    @property
    def source_context(self) -> str:
        return "regulatory_reporting"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "submission_ref": self.submission_ref,
            "country_code": self.country_code,
            "regulator_type": self.regulator_type,
            "export_format": self.export_format,
        }


@dataclass(frozen=True, kw_only=True)
class DigitalSubmissionSubmittedIntegration(IntegrationEvent):
    submission_ref: str
    portal_reference: str

    @property
    def event_name(self) -> str:
        return "regulatory.submission.submitted"

    @property
    def source_context(self) -> str:
        return "regulatory_reporting"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "submission_ref": self.submission_ref,
            "portal_reference": self.portal_reference,
        }
