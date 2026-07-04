"""Policy decision DTO and evaluator port."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    matched: bool
    policy_id: str | None
    version: int | None
    outcome: str | None
    parameters: dict
    applied_exception: str | None
    evaluation_trace: list[dict]

    @classmethod
    def from_evaluation(cls, data: dict) -> PolicyDecision:
        return cls(
            matched=bool(data.get("matched")),
            policy_id=data.get("policy_id"),
            version=data.get("version"),
            outcome=data.get("outcome"),
            parameters=data.get("parameters") or {},
            applied_exception=data.get("applied_exception"),
            evaluation_trace=data.get("evaluation_trace") or [],
        )

    def to_dict(self) -> dict:
        return {
            "matched": self.matched,
            "policy_id": self.policy_id,
            "version": self.version,
            "outcome": self.outcome,
            "parameters": self.parameters,
            "applied_exception": self.applied_exception,
            "evaluation_trace": self.evaluation_trace,
        }


class IPolicyEvaluator(Protocol):
    async def evaluate(
        self,
        *,
        tenant_id: str,
        domain: str,
        policy_key: str,
        facts: dict,
        as_of: datetime | None = None,
        organization_id: str | None = None,
    ) -> PolicyDecision: ...
