"""Quality / governance commands (P200-B12)."""
from __future__ import annotations

from dataclasses import dataclass, field

from contexts.identity_federation.domain.services.federation_quality_platform import (
    get_federation_quality_platform,
)
from contexts.identity_federation.infrastructure.observability import (
    federation_quality_metrics,
)


@dataclass(frozen=True, slots=True)
class RecordQualityAssessmentCommand:
    tenant_id: str
    assessor: str = "ci"
    checklist_ids: list[str] = field(default_factory=list)
    passed: bool = True
    notes: str = ""


@dataclass(frozen=True, slots=True)
class EvaluateQualityGateCommand:
    tenant_id: str
    gate_id: str
    evidence: dict = field(default_factory=dict)
    passed: bool | None = None


@dataclass(frozen=True, slots=True)
class CertifyReleaseCommand:
    tenant_id: str
    version: str = "1.0.0"
    boards_approved: list[str] = field(default_factory=list)
    require_core_series: bool = True


async def handle_record_quality_assessment(
    cmd: RecordQualityAssessmentCommand,
) -> dict:
    federation_quality_metrics.increment("qa_command_assessment_total")
    return get_federation_quality_platform().record_assessment(
        tenant_id=cmd.tenant_id,
        assessor=cmd.assessor,
        checklist_ids=cmd.checklist_ids or None,
        passed=cmd.passed,
        notes=cmd.notes,
    )


async def handle_evaluate_quality_gate(cmd: EvaluateQualityGateCommand) -> dict:
    federation_quality_metrics.increment("qa_command_gate_total")
    return get_federation_quality_platform().evaluate_gate(
        tenant_id=cmd.tenant_id,
        gate_id=cmd.gate_id,
        evidence=cmd.evidence,
        passed=cmd.passed,
    )


async def handle_certify_release(cmd: CertifyReleaseCommand) -> dict:
    federation_quality_metrics.increment("qa_command_certify_total")
    return get_federation_quality_platform().certify_release(
        tenant_id=cmd.tenant_id,
        version=cmd.version,
        boards_approved=cmd.boards_approved or None,
        require_core_series=cmd.require_core_series,
    )
