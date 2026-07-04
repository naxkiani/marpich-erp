"""Municipality integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class PermitIssuedIntegration(IntegrationEvent):
    permit_id: UniqueId
    permit_type: str
    applicant_name: str

    @property
    def event_name(self) -> str:
        return "municipality.permit.issued"

    @property
    def source_context(self) -> str:
        return "municipality"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "permit_id": str(self.permit_id),
            "permit_type": self.permit_type,
            "applicant_name": self.applicant_name,
        }


@dataclass(frozen=True, kw_only=True)
class ServiceRequestClosedIntegration(IntegrationEvent):
    request_id: UniqueId
    category: str
    resolution: str

    @property
    def event_name(self) -> str:
        return "municipality.service.request.closed"

    @property
    def source_context(self) -> str:
        return "municipality"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "request_id": str(self.request_id),
            "category": self.category,
            "resolution": self.resolution,
        }


@dataclass(frozen=True, kw_only=True)
class UtilityBillIssuedIntegration(IntegrationEvent):
    account_id: UniqueId
    account_number: str
    utility_type: str
    amount: str
    period: str

    @property
    def event_name(self) -> str:
        return "municipality.utility.bill.issued"

    @property
    def source_context(self) -> str:
        return "municipality"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "account_id": str(self.account_id),
            "account_number": self.account_number,
            "utility_type": self.utility_type,
            "amount": self.amount,
            "period": self.period,
        }
