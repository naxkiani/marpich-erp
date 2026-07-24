"""Federation CQRS buses — tenant, idempotency, correlation middleware (P200-B10)."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

CommandHandler = Callable[..., Awaitable[dict]]
QueryHandler = Callable[..., Awaitable[dict]] | Callable[..., dict]


@dataclass(frozen=True, slots=True)
class BusEnvelope:
    tenant_id: str
    name: str
    payload: dict = field(default_factory=dict)
    correlation_id: str = ""
    idempotency_key: str = ""
    user_id: str | None = None


class FederationCommandBus:
    def __init__(self) -> None:
        self._handlers: dict[str, CommandHandler] = {}
        self._idempotency: dict[str, dict] = {}

    def register(self, name: str, handler: CommandHandler) -> None:
        self._handlers[name] = handler

    def catalog(self) -> list[str]:
        return sorted(self._handlers)

    async def dispatch(self, envelope: BusEnvelope) -> dict:
        if not envelope.tenant_id:
            raise ValueError("cqrs.tenant_required")
        if envelope.name not in self._handlers:
            raise ValueError(f"cqrs.command_unknown:{envelope.name}")
        corr = envelope.correlation_id or str(uuid4())
        if envelope.idempotency_key:
            cache_key = f"{envelope.tenant_id}:{envelope.name}:{envelope.idempotency_key}"
            if cache_key in self._idempotency:
                return {
                    **self._idempotency[cache_key],
                    "idempotent_replay": True,
                    "correlation_id": corr,
                }
        result = await self._handlers[envelope.name](envelope)
        wrapped = {
            "result": result,
            "command": envelope.name,
            "tenant_id": envelope.tenant_id,
            "correlation_id": corr,
            "idempotent_replay": False,
            "dispatched_at": datetime.now(UTC).isoformat(),
        }
        if envelope.idempotency_key:
            self._idempotency[f"{envelope.tenant_id}:{envelope.name}:{envelope.idempotency_key}"] = (
                wrapped
            )
        return wrapped

    def reset(self) -> None:
        self._idempotency.clear()


class FederationQueryBus:
    def __init__(self) -> None:
        self._handlers: dict[str, QueryHandler] = {}

    def register(self, name: str, handler: QueryHandler) -> None:
        self._handlers[name] = handler

    def catalog(self) -> list[str]:
        return sorted(self._handlers)

    async def dispatch(self, envelope: BusEnvelope) -> dict:
        if not envelope.tenant_id:
            raise ValueError("cqrs.tenant_required")
        if envelope.name not in self._handlers:
            raise ValueError(f"cqrs.query_unknown:{envelope.name}")
        corr = envelope.correlation_id or str(uuid4())
        handler = self._handlers[envelope.name]
        outcome = handler(envelope)
        if isinstance(outcome, dict):
            result = outcome
        else:
            result = await outcome  # type: ignore[misc]
        return {
            "result": result,
            "query": envelope.name,
            "tenant_id": envelope.tenant_id,
            "correlation_id": corr,
            "dispatched_at": datetime.now(UTC).isoformat(),
        }


_command_bus: FederationCommandBus | None = None
_query_bus: FederationQueryBus | None = None


def get_command_bus() -> FederationCommandBus:
    global _command_bus
    if _command_bus is None:
        _command_bus = FederationCommandBus()
        _register_default_commands(_command_bus)
    return _command_bus


def get_query_bus() -> FederationQueryBus:
    global _query_bus
    if _query_bus is None:
        _query_bus = FederationQueryBus()
        _register_default_queries(_query_bus)
    return _query_bus


def reset_federation_buses() -> None:
    global _command_bus, _query_bus
    if _command_bus is not None:
        _command_bus.reset()
    _command_bus = None
    _query_bus = None


def _register_default_commands(bus: FederationCommandBus) -> None:
    async def _evaluate_zt(env: BusEnvelope) -> dict:
        from contexts.identity_federation.application.commands.security_control_commands import (
            EvaluateZeroTrustCommand,
            handle_evaluate_zero_trust,
        )

        return await handle_evaluate_zero_trust(
            EvaluateZeroTrustCommand(tenant_id=env.tenant_id, context=dict(env.payload))
        )

    async def _request_trust(env: BusEnvelope) -> dict:
        from contexts.identity_federation.application.commands.cross_tenant_commands import (
            RequestTenantTrustCommand,
            handle_request_tenant_trust,
        )
        from contexts.identity_federation.container import get_tenant_federation_repository

        return await handle_request_tenant_trust(
            RequestTenantTrustCommand(
                tenant_id=env.tenant_id,
                partner_tenant_id=str(env.payload.get("partner_tenant_id") or ""),
                assess_inputs=dict(env.payload.get("assess_inputs") or {}),
                agreement=dict(env.payload.get("agreement") or {}),
            ),
            tenant_feds=get_tenant_federation_repository(),
        )

    async def _detect_threat(env: BusEnvelope) -> dict:
        from contexts.identity_federation.application.commands.security_control_commands import (
            DetectThreatCommand,
            handle_detect_threat,
        )

        return await handle_detect_threat(
            DetectThreatCommand(tenant_id=env.tenant_id, indicators=dict(env.payload))
        )

    async def _signal_incident(env: BusEnvelope) -> dict:
        from contexts.identity_federation.application.commands.ops_commands import (
            SignalIncidentCommand,
            handle_signal_incident,
        )

        return await handle_signal_incident(
            SignalIncidentCommand(
                tenant_id=env.tenant_id,
                incident_class=str(env.payload.get("incident_class") or "federation_outage"),
                severity=str(env.payload.get("severity") or "medium"),
                summary=str(env.payload.get("summary") or ""),
                signals=dict(env.payload.get("signals") or {}),
            )
        )

    async def _record_dr(env: BusEnvelope) -> dict:
        from contexts.identity_federation.application.commands.ops_commands import (
            RecordDrDrillCommand,
            handle_record_dr_drill,
        )

        return await handle_record_dr_drill(
            RecordDrDrillCommand(
                tenant_id=env.tenant_id,
                mode=str(env.payload.get("mode") or "active_passive"),
                steps_completed=list(env.payload.get("steps_completed") or []),
                passed=bool(env.payload.get("passed", True)),
                notes=str(env.payload.get("notes") or ""),
            )
        )

    async def _ai_ops(env: BusEnvelope) -> dict:
        from contexts.identity_federation.application.commands.ops_commands import (
            RequestAiOpsRecommendationCommand,
            handle_request_ai_ops_recommendation,
        )

        return await handle_request_ai_ops_recommendation(
            RequestAiOpsRecommendationCommand(
                tenant_id=env.tenant_id,
                context=dict(env.payload),
            )
        )

    bus.register("EvaluateZeroTrust", _evaluate_zt)
    bus.register("RequestTenantTrust", _request_trust)
    bus.register("DetectThreat", _detect_threat)
    async def _qa_assess(env: BusEnvelope) -> dict:
        from contexts.identity_federation.application.commands.qa_commands import (
            RecordQualityAssessmentCommand,
            handle_record_quality_assessment,
        )

        return await handle_record_quality_assessment(
            RecordQualityAssessmentCommand(
                tenant_id=env.tenant_id,
                assessor=str(env.payload.get("assessor") or "ci"),
                checklist_ids=list(env.payload.get("checklist_ids") or []),
                passed=bool(env.payload.get("passed", True)),
                notes=str(env.payload.get("notes") or ""),
            )
        )

    async def _qa_gate(env: BusEnvelope) -> dict:
        from contexts.identity_federation.application.commands.qa_commands import (
            EvaluateQualityGateCommand,
            handle_evaluate_quality_gate,
        )

        passed = env.payload.get("passed")
        return await handle_evaluate_quality_gate(
            EvaluateQualityGateCommand(
                tenant_id=env.tenant_id,
                gate_id=str(env.payload.get("gate_id") or ""),
                evidence=dict(env.payload.get("evidence") or {}),
                passed=None if passed is None else bool(passed),
            )
        )

    async def _qa_certify(env: BusEnvelope) -> dict:
        from contexts.identity_federation.application.commands.qa_commands import (
            CertifyReleaseCommand,
            handle_certify_release,
        )

        return await handle_certify_release(
            CertifyReleaseCommand(
                tenant_id=env.tenant_id,
                version=str(env.payload.get("version") or "1.0.0"),
                boards_approved=list(env.payload.get("boards_approved") or []),
                require_core_series=bool(env.payload.get("require_core_series", True)),
            )
        )

    bus.register("SignalIncident", _signal_incident)
    bus.register("RecordDrDrill", _record_dr)
    bus.register("RequestAiOpsRecommendation", _ai_ops)
    bus.register("RecordQualityAssessment", _qa_assess)
    bus.register("EvaluateQualityGate", _qa_gate)
    bus.register("CertifyRelease", _qa_certify)


def _register_default_queries(bus: FederationQueryBus) -> None:
    def _posture(env: BusEnvelope) -> dict:
        from contexts.identity_federation.application.queries.security_control_queries import (
            handle_get_security_posture,
        )

        return handle_get_security_posture(tenant_id=env.tenant_id)

    def _ohs(env: BusEnvelope) -> dict:
        from contexts.identity_federation.domain.services.federation_ohs_platform import (
            get_federation_ohs_platform,
        )

        return get_federation_ohs_platform().catalog()

    def _ops_surface(env: BusEnvelope) -> dict:
        from contexts.identity_federation.domain.services.federation_ops_platform import (
            get_federation_ops_platform,
        )

        return get_federation_ops_platform().surface()

    def _ops_slo(env: BusEnvelope) -> dict:
        from contexts.identity_federation.domain.services.federation_ops_platform import (
            get_federation_ops_platform,
        )

        ratio = env.payload.get("availability_ratio")
        return get_federation_ops_platform().slo_status(
            availability_ratio=float(ratio) if ratio is not None else None
        )

    def _ops_health(env: BusEnvelope) -> dict:
        from contexts.identity_federation.domain.services.federation_ops_platform import (
            get_federation_ops_platform,
        )

        return get_federation_ops_platform().health()

    bus.register("GetSecurityPosture", _posture)
    bus.register("GetOhsCatalog", _ohs)
    def _qa_surface(env: BusEnvelope) -> dict:
        from contexts.identity_federation.domain.services.federation_quality_platform import (
            get_federation_quality_platform,
        )

        return get_federation_quality_platform().surface()

    def _qa_readiness(env: BusEnvelope) -> dict:
        from contexts.identity_federation.domain.services.federation_quality_platform import (
            get_federation_quality_platform,
        )

        return get_federation_quality_platform().production_readiness()

    bus.register("GetOpsSurface", _ops_surface)
    bus.register("GetSloStatus", _ops_slo)
    bus.register("GetOpsHealth", _ops_health)
    bus.register("GetQaSurface", _qa_surface)
    bus.register("GetProductionReadiness", _qa_readiness)
