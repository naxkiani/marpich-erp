"""Federation saga orchestration — trust establishment / IdP activation (P200-B10)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from uuid import uuid4


@dataclass
class FederationSaga:
    saga_ref: str
    tenant_id: str
    saga_type: str
    status: str = "running"  # running|completed|compensating|compensated|failed|timed_out
    steps: list[dict] = field(default_factory=list)
    context: dict = field(default_factory=dict)
    expires_at: datetime = field(default_factory=lambda: datetime.now(UTC) + timedelta(hours=1))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        return {
            "saga_ref": self.saga_ref,
            "tenant_id": self.tenant_id,
            "saga_type": self.saga_type,
            "status": self.status,
            "steps": self.steps,
            "context": self.context,
            "expires_at": self.expires_at.isoformat(),
        }


class FederationSagaEngine:
    SAGA_TYPES = {
        "federation_trust_establishment": [
            "assess_trust",
            "await_approval",
            "activate_trust",
        ],
        "identity_provider_activation": [
            "verify_provider",
            "evaluate_trust",
            "activate_provider",
        ],
    }

    def __init__(self) -> None:
        self._sagas: dict[str, FederationSaga] = {}

    def start(
        self,
        *,
        tenant_id: str,
        saga_type: str,
        context: dict | None = None,
        timeout_minutes: int = 60,
    ) -> dict:
        if saga_type not in self.SAGA_TYPES:
            raise ValueError("saga.unknown_type")
        if not tenant_id:
            raise ValueError("saga.tenant_required")
        ref = f"saga-{uuid4().hex[:10]}"
        steps = [
            {"name": name, "status": "pending"} for name in self.SAGA_TYPES[saga_type]
        ]
        steps[0]["status"] = "completed"
        steps[0]["at"] = datetime.now(UTC).isoformat()
        saga = FederationSaga(
            saga_ref=ref,
            tenant_id=tenant_id,
            saga_type=saga_type,
            steps=steps,
            context=context or {},
            expires_at=datetime.now(UTC) + timedelta(minutes=max(1, timeout_minutes)),
        )
        self._sagas[f"{tenant_id}:{ref}"] = saga
        return saga.to_dict()

    def advance(self, *, tenant_id: str, saga_ref: str, step_ok: bool = True) -> dict:
        saga = self._get(tenant_id, saga_ref)
        self._check_timeout(saga)
        if saga.status != "running":
            raise ValueError("saga.not_running")
        pending = next((s for s in saga.steps if s["status"] == "pending"), None)
        if pending is None:
            saga.status = "completed"
            return saga.to_dict()
        if not step_ok:
            return self.compensate(tenant_id=tenant_id, saga_ref=saga_ref, reason="step_failed")
        pending["status"] = "completed"
        pending["at"] = datetime.now(UTC).isoformat()
        if all(s["status"] == "completed" for s in saga.steps):
            saga.status = "completed"
        return saga.to_dict()

    def compensate(self, *, tenant_id: str, saga_ref: str, reason: str = "") -> dict:
        saga = self._get(tenant_id, saga_ref)
        saga.status = "compensating"
        for step in reversed(saga.steps):
            if step["status"] == "completed":
                step["status"] = "compensated"
                step["compensation_reason"] = reason
                step["compensated_at"] = datetime.now(UTC).isoformat()
        saga.status = "compensated"
        saga.context = {**(saga.context or {}), "compensation_reason": reason}
        return saga.to_dict()

    def get(self, *, tenant_id: str, saga_ref: str) -> dict:
        return self._get(tenant_id, saga_ref).to_dict()

    def _get(self, tenant_id: str, saga_ref: str) -> FederationSaga:
        saga = self._sagas.get(f"{tenant_id}:{saga_ref}")
        if saga is None:
            raise ValueError("saga.not_found")
        self._check_timeout(saga)
        return saga

    def _check_timeout(self, saga: FederationSaga) -> None:
        if saga.status == "running" and saga.expires_at <= datetime.now(UTC):
            saga.status = "timed_out"

    def reset(self) -> None:
        self._sagas.clear()


_engine: FederationSagaEngine | None = None


def get_federation_saga_engine() -> FederationSagaEngine:
    global _engine
    if _engine is None:
        _engine = FederationSagaEngine()
    return _engine


def reset_federation_saga_engine() -> None:
    global _engine
    if _engine is not None:
        _engine.reset()
    _engine = None
