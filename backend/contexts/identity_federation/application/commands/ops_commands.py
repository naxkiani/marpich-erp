"""Operations commands — incidents, DR drills, AI ops signals (P200-B11)."""
from __future__ import annotations

from dataclasses import dataclass, field

from contexts.identity_federation.domain.services.federation_ops_platform import (
    get_federation_ops_platform,
)
from contexts.identity_federation.infrastructure.observability import federation_ops_metrics


@dataclass(frozen=True, slots=True)
class SignalIncidentCommand:
    tenant_id: str
    incident_class: str = "federation_outage"
    severity: str = "medium"
    summary: str = ""
    signals: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RecordDrDrillCommand:
    tenant_id: str
    mode: str = "active_passive"
    steps_completed: list[str] = field(default_factory=list)
    passed: bool = True
    notes: str = ""


@dataclass(frozen=True, slots=True)
class RequestAiOpsRecommendationCommand:
    tenant_id: str
    context: dict = field(default_factory=dict)


async def handle_signal_incident(cmd: SignalIncidentCommand) -> dict:
    federation_ops_metrics.increment("ops_command_signal_incident_total")
    return get_federation_ops_platform().signal_incident(
        tenant_id=cmd.tenant_id,
        incident_class=cmd.incident_class,
        severity=cmd.severity,
        summary=cmd.summary,
        signals=cmd.signals,
    )


async def handle_record_dr_drill(cmd: RecordDrDrillCommand) -> dict:
    federation_ops_metrics.increment("ops_command_dr_drill_total")
    return get_federation_ops_platform().record_dr_drill(
        tenant_id=cmd.tenant_id,
        mode=cmd.mode,
        steps_completed=cmd.steps_completed,
        passed=cmd.passed,
        notes=cmd.notes,
    )


async def handle_request_ai_ops_recommendation(
    cmd: RequestAiOpsRecommendationCommand,
) -> dict:
    federation_ops_metrics.increment("ops_command_ai_recommend_total")
    return get_federation_ops_platform().recommend_ai_ops(
        tenant_id=cmd.tenant_id,
        context=cmd.context,
    )
