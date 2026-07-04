"""Hospital integration event adapter port."""
from __future__ import annotations

from typing import Protocol

from contexts.accounting.application.commands.create_billing_from_encounter import (
    CreateBillingFromEncounterCommand,
)


class IHospitalEventAdapter(Protocol):
    async def parse_encounter_completed(
        self, envelope: dict
    ) -> CreateBillingFromEncounterCommand: ...
