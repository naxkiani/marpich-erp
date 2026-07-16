"""Authorization decision DTO and evaluator port (PEP for modules)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True, slots=True)
class AccessDecision:
    decision: str
    obligations: list[str] = field(default_factory=list)
    reason_codes: list[str] = field(default_factory=list)
    model: str | None = None
    permission_code: str | None = None
    evaluation_trace: list[dict] = field(default_factory=list)

    @property
    def allowed(self) -> bool:
        return self.decision == "allow"

    @classmethod
    def from_payload(cls, data: dict) -> AccessDecision:
        return cls(
            decision=str(data.get("decision") or "deny"),
            obligations=list(data.get("obligations") or []),
            reason_codes=list(data.get("reason_codes") or []),
            model=data.get("model"),
            permission_code=data.get("permission_code"),
            evaluation_trace=list(data.get("evaluation_trace") or []),
        )

    def to_dict(self) -> dict:
        return {
            "decision": self.decision,
            "obligations": self.obligations,
            "reason_codes": self.reason_codes,
            "model": self.model,
            "permission_code": self.permission_code,
            "evaluation_trace": self.evaluation_trace,
        }


class IAuthorizationEvaluator(Protocol):
    async def check_access(
        self,
        tenant_id: str,
        *,
        principal_id: str,
        resource: str = "",
        action: str = "",
        permission_code: str | None = None,
        context: dict | None = None,
        simulate: bool = False,
        record: bool = True,
    ) -> AccessDecision: ...

    async def write_relation(
        self,
        tenant_id: str,
        *,
        subject_type: str,
        subject_id: str,
        relation: str,
        object_type: str,
        object_id: str,
        tuple_ref: str | None = None,
    ) -> bool: ...
