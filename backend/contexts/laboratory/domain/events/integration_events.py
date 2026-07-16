"""Laboratory integration events — CAP-HLT-007 published language."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class SampleReceivedIntegration(IntegrationEvent):
    sample_id: UniqueId
    order_id: UniqueId
    accession_number: str
    patient_ref: str

    @property
    def event_name(self) -> str:
        return "laboratory.sample.received"

    @property
    def source_context(self) -> str:
        return "laboratory"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "sample_id": str(self.sample_id),
            "order_id": str(self.order_id),
            "accession_number": self.accession_number,
            "patient_ref": self.patient_ref,
        }


@dataclass(frozen=True, kw_only=True)
class ResultAvailableIntegration(IntegrationEvent):
    order_id: UniqueId
    patient_ref: str
    test_code: str
    result_value: str
    result_unit: str | None

    @property
    def event_name(self) -> str:
        return "laboratory.result.available"

    @property
    def source_context(self) -> str:
        return "laboratory"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "order_id": str(self.order_id),
            "patient_ref": self.patient_ref,
            "test_code": self.test_code,
            "result_value": self.result_value,
            "result_unit": self.result_unit,
        }
