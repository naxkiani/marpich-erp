"""ACL — translate platform events to notification commands."""
from __future__ import annotations

from contexts.notifications.application.commands.deliver_from_event import DeliverFromEventCommand


def _format(template: str, values: dict) -> str:
    result = template
    for key, val in values.items():
        result = result.replace("{" + key + "}", str(val))
    return result


class NotificationEventAdapter:
    async def parse_integration_event(self, envelope: dict) -> DeliverFromEventCommand | None:
        event_name = envelope.get("event_name", "")
        payload = envelope.get("payload", {})
        tenant_id = envelope["tenant_id"]
        correlation_id = envelope["correlation_id"]

        if event_name == "identity.user.created":
            return DeliverFromEventCommand(
                tenant_id=tenant_id,
                correlation_id=correlation_id,
                source_event=event_name,
                user_id=payload.get("user_id"),
                recipient_email=payload.get("email"),
                template_key="welcome",
                title=_format("Welcome to {tenant_id}", {"tenant_id": tenant_id}),
                body=_format(
                    "Hello {display_name}, your account ({email}) is ready.",
                    {
                        "display_name": payload.get("display_name", "User"),
                        "email": payload.get("email", ""),
                    },
                ),
                category="onboarding",
                channel="inbox",
            )

        if event_name == "platform.tenant.provisioned":
            return DeliverFromEventCommand(
                tenant_id=tenant_id,
                correlation_id=correlation_id,
                source_event=event_name,
                user_id=None,
                recipient_email=None,
                template_key="tenant_provisioned",
                title=_format("Tenant {name} is ready", {"name": payload.get("name", tenant_id)}),
                body=_format(
                    "Industry pack {pack} activated with {count} modules.",
                    {
                        "pack": payload.get("industry_pack", ""),
                        "count": len(payload.get("enabled_modules", [])),
                    },
                ),
                category="platform",
                channel="inbox",
            )

        if event_name == "hospital.encounter.completed":
            return DeliverFromEventCommand(
                tenant_id=tenant_id,
                correlation_id=correlation_id,
                source_event=event_name,
                user_id=None,
                recipient_email=None,
                template_key="encounter_completed",
                title="Clinical encounter completed",
                body=_format(
                    "Encounter {encounter_id} completed. Procedures: {codes}",
                    {
                        "encounter_id": payload.get("encounter_id", ""),
                        "codes": ", ".join(payload.get("procedure_codes", [])) or "none",
                    },
                ),
                category="healthcare",
                channel="inbox",
            )

        if event_name == "finance.journal.recorded":
            return DeliverFromEventCommand(
                tenant_id=tenant_id,
                correlation_id=correlation_id,
                source_event=event_name,
                user_id=None,
                recipient_email=None,
                template_key="journal_recorded",
                title="GL journal recorded",
                body=_format(
                    "Journal posted for {source_type} {source_id}.",
                    {
                        "source_type": payload.get("source_type", ""),
                        "source_id": payload.get("source_id", ""),
                    },
                ),
                category="finance",
                channel="inbox",
            )

        if event_name == "workflow.task.assigned":
            return DeliverFromEventCommand(
                tenant_id=tenant_id,
                correlation_id=correlation_id,
                source_event=event_name,
                user_id=payload.get("assignee_id"),
                recipient_email=None,
                template_key="task_assigned",
                title=_format("Task: {step_name}", {"step_name": payload.get("step_name", "Approval")}),
                body=_format(
                    "You have a pending workflow task ({step_key}) on instance {instance_id}.",
                    {
                        "step_key": payload.get("step_key", ""),
                        "instance_id": payload.get("instance_id", ""),
                    },
                ),
                category="workflow",
                channel="inbox",
            )

        return None


async def on_integration_event(envelope: dict) -> DeliverFromEventCommand | None:
    return await NotificationEventAdapter().parse_integration_event(envelope)
