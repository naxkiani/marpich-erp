"""AI application service — platform assist (no vendor SDK in modules)."""
from __future__ import annotations

from contexts.ai.domain.aggregates.assist_session import AssistSession
from contexts.ai.domain.events.integration_events import InsightGeneratedIntegration
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class AiApplicationService:
    def __init__(self) -> None:
        self._sessions: dict[str, AssistSession] = {}

    def reset(self) -> None:
        self._sessions.clear()

    async def assist(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        module_id: str,
        surface: str,
        prompt: str,
        actor_user_id: str | None = None,
        context: dict | None = None,
    ) -> Result[dict]:
        text = (prompt or "").strip()
        if not text:
            return Result.fail("ai.errors.empty_prompt")
        ctx = context or {}
        refs = []
        for key in ("student_id", "course_id", "document_id", "sale_id"):
            if ctx.get(key):
                refs.append(f"{key}={ctx[key]}")
        ref_note = f" Context refs: {', '.join(refs)}." if refs else ""
        reply = (
            f"[Marpich AI · {module_id}/{surface}] I received your question about "
            f"«{text[:180]}».{ref_note} "
            "This is the Core AI platform assist surface — provider models are wired "
            "through the AI Service, not embedded in business modules."
        )
        session = AssistSession.create(
            tenant_id=tenant_id,
            module_id=module_id,
            surface=surface,
            prompt=text,
            reply=reply,
            actor_user_id=actor_user_id,
        )
        self._sessions[str(session.id)] = session
        await publish_integration_event(
            InsightGeneratedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                actor_user_id=actor_user_id,
                session_id=session.id,
                module_id=session.module_id,
                surface=session.surface,
                summary=reply[:240],
            )
        )
        return Result.ok(session.to_dict())
