"""AI assist session — platform LLM orchestration ACL surface."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class AssistSession(AggregateRoot):
    tenant_id: str
    module_id: str
    surface: str
    prompt: str
    reply: str
    actor_user_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        module_id: str,
        surface: str,
        prompt: str,
        reply: str,
        actor_user_id: str | None = None,
    ) -> AssistSession:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            module_id=module_id.strip() or "platform",
            surface=surface.strip() or "assistant",
            prompt=prompt.strip(),
            reply=reply.strip(),
            actor_user_id=actor_user_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "module_id": self.module_id,
            "surface": self.surface,
            "prompt": self.prompt,
            "reply": self.reply,
            "actor_user_id": self.actor_user_id,
            "created_at": self.created_at.isoformat(),
        }
