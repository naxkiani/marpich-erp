"""Ports — peer care-event envelope adapters (ACL implements; application depends on port)."""
from __future__ import annotations

from typing import Protocol

from contexts.hospital.application.commands.record_care_event import (
    RecordLabResultCareEventCommand,
    RecordPharmacyDispenseCareEventCommand,
)


class ILaboratoryEventAdapter(Protocol):
    def parse_result_available(self, envelope: dict) -> RecordLabResultCareEventCommand: ...


class IPharmacyEventAdapter(Protocol):
    def parse_dispense_completed(
        self, envelope: dict
    ) -> RecordPharmacyDispenseCareEventCommand: ...
