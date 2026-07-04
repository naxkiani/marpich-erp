"""Feature flag DTO and evaluator port."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class FlagEvaluation:
    enabled: bool
    variant_id: str | None
    reason: str
    flag_version: int

    @classmethod
    def from_dict(cls, data: dict) -> FlagEvaluation:
        return cls(
            enabled=bool(data.get("enabled")),
            variant_id=data.get("variant_id"),
            reason=str(data.get("reason", "default")),
            flag_version=int(data.get("flag_version", 0)),
        )

    def to_dict(self) -> dict:
        return {
            "enabled": self.enabled,
            "variant_id": self.variant_id,
            "reason": self.reason,
            "flag_version": self.flag_version,
        }


class IFeatureFlagEvaluator(Protocol):
    async def evaluate(
        self,
        *,
        tenant_id: str,
        keys: list[str],
        context: dict | None = None,
    ) -> dict[str, FlagEvaluation]: ...

    async def is_enabled(
        self,
        *,
        tenant_id: str,
        key: str,
        context: dict | None = None,
    ) -> bool: ...
