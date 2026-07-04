"""ACL — translate Hospital events to Accounting commands."""
from __future__ import annotations

from contexts.accounting.application.commands.create_billing_from_encounter import (
    CreateBillingFromEncounterCommand,
)


class HospitalEventAdapter:
    async def parse_encounter_completed(
        self, envelope: dict
    ) -> CreateBillingFromEncounterCommand:
        payload = envelope["payload"]
        return CreateBillingFromEncounterCommand(
            tenant_id=envelope["tenant_id"],
            correlation_id=envelope["correlation_id"],
            external_encounter_id=payload["encounter_id"],
            patient_ref=payload["patient_id"],
            procedure_codes=list(payload.get("procedure_codes", [])),
        )


async def on_encounter_completed(envelope: dict) -> CreateBillingFromEncounterCommand:
    return await HospitalEventAdapter().parse_encounter_completed(envelope)
