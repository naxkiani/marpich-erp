"""PostgreSQL repositories — Identity Risk SoR."""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select

from contexts.identity_risk.domain.aggregates.identity_risk_platform import (
    AnomalyAlert,
    RiskProfile,
    RiskScore,
    RiskSignal,
)
from contexts.identity_risk.domain.ports.identity_risk_repositories import (
    IAnomalyAlertRepository,
    IRiskProfileRepository,
    IRiskScoreRepository,
    IRiskSignalRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    IdentityRiskAlertRow,
    IdentityRiskProfileRow,
    IdentityRiskScoreRow,
    IdentityRiskSignalRow,
)


def _uuid(value: UniqueId | str | UUID) -> UUID:
    if isinstance(value, UUID):
        return value
    return UUID(str(value))


class _RefCounterMixin:
    _local_counters: dict[str, int] = {}

    def _local_next(self, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        n = self._local_counters.get(key, 0) + 1
        self._local_counters[key] = n
        return f"{prefix}-{tenant_id}-{n:04d}"

    @classmethod
    def reset_counters(cls) -> None:
        cls._local_counters = {}


def _profile_from_row(row: object) -> RiskProfile:
    return RiskProfile(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        profile_ref=row.profile_ref,
        scoring_enabled=bool(row.scoring_enabled),
        score_threshold=int(row.score_threshold),
        step_up_threshold=int(row.step_up_threshold),
        bulk_create_threshold=int(row.bulk_create_threshold),
        created_at=row.created_at or datetime.now(UTC),
    )


def _signal_from_row(row: object) -> RiskSignal:
    return RiskSignal(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        signal_ref=row.signal_ref,
        source=row.source,
        event_name=row.event_name,
        user_id=row.user_id,
        factors=list(row.factors or []),
        raw_payload=dict(row.raw_payload or {}),
        created_at=row.created_at or datetime.now(UTC),
    )


def _score_from_row(row: object) -> RiskScore:
    return RiskScore(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        score_ref=row.score_ref,
        signal_ref=row.signal_ref,
        score=int(row.score),
        risk_level=row.risk_level,
        explanation=row.explanation,
        factors=list(row.factors or []),
        step_up_recommended=bool(row.step_up_recommended),
        user_id=row.user_id,
        created_at=row.created_at or datetime.now(UTC),
    )


def _alert_from_row(row: object) -> AnomalyAlert:
    return AnomalyAlert(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        alert_ref=row.alert_ref,
        score_ref=row.score_ref,
        title=row.title,
        severity=row.severity,
        description=row.description,
        acknowledged=bool(row.acknowledged),
        created_at=row.created_at or datetime.now(UTC),
    )


class PostgresRiskProfileRepository(IRiskProfileRepository, _RefCounterMixin):
    async def find_by_tenant(self, tenant_id: str) -> RiskProfile | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(IdentityRiskProfileRow).where(IdentityRiskProfileRow.tenant_id == tenant_id)
            )
            return _profile_from_row(row) if row else None

    async def save(self, profile: RiskProfile) -> None:
        async with session_scope(tenant_id=profile.tenant_id) as session:
            row = await session.get(IdentityRiskProfileRow, (profile.tenant_id, _uuid(profile.id)))
            if row is None:
                session.add(
                    IdentityRiskProfileRow(
                        tenant_id=profile.tenant_id,
                        id=_uuid(profile.id),
                        profile_ref=profile.profile_ref,
                        scoring_enabled=profile.scoring_enabled,
                        score_threshold=profile.score_threshold,
                        step_up_threshold=profile.step_up_threshold,
                        bulk_create_threshold=profile.bulk_create_threshold,
                        created_at=profile.created_at,
                    )
                )
            else:
                row.profile_ref = profile.profile_ref
                row.scoring_enabled = profile.scoring_enabled
                row.score_threshold = profile.score_threshold
                row.step_up_threshold = profile.step_up_threshold
                row.bulk_create_threshold = profile.bulk_create_threshold

    def next_profile_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "risk-profile")


class PostgresRiskSignalRepository(IRiskSignalRepository, _RefCounterMixin):
    async def save(self, signal: RiskSignal) -> None:
        async with session_scope(tenant_id=signal.tenant_id) as session:
            row = await session.get(IdentityRiskSignalRow, (signal.tenant_id, _uuid(signal.id)))
            if row is None:
                session.add(
                    IdentityRiskSignalRow(
                        tenant_id=signal.tenant_id,
                        id=_uuid(signal.id),
                        signal_ref=signal.signal_ref,
                        source=signal.source,
                        event_name=signal.event_name,
                        user_id=signal.user_id,
                        factors=list(signal.factors or []),
                        raw_payload=dict(signal.raw_payload or {}),
                        created_at=signal.created_at,
                    )
                )
            else:
                row.signal_ref = signal.signal_ref
                row.source = signal.source
                row.event_name = signal.event_name
                row.user_id = signal.user_id
                row.factors = list(signal.factors or [])
                row.raw_payload = dict(signal.raw_payload or {})

    async def list_by_tenant(self, tenant_id: str) -> list[RiskSignal]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(IdentityRiskSignalRow).where(IdentityRiskSignalRow.tenant_id == tenant_id)
                )
            ).all()
        return [_signal_from_row(r) for r in rows]

    def next_signal_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "signal")


class PostgresRiskScoreRepository(IRiskScoreRepository, _RefCounterMixin):
    async def save(self, score: RiskScore) -> None:
        async with session_scope(tenant_id=score.tenant_id) as session:
            row = await session.get(IdentityRiskScoreRow, (score.tenant_id, _uuid(score.id)))
            if row is None:
                session.add(
                    IdentityRiskScoreRow(
                        tenant_id=score.tenant_id,
                        id=_uuid(score.id),
                        score_ref=score.score_ref,
                        signal_ref=score.signal_ref,
                        score=score.score,
                        risk_level=score.risk_level,
                        explanation=score.explanation,
                        factors=list(score.factors or []),
                        step_up_recommended=score.step_up_recommended,
                        user_id=score.user_id,
                        created_at=score.created_at,
                    )
                )
            else:
                row.score_ref = score.score_ref
                row.signal_ref = score.signal_ref
                row.score = score.score
                row.risk_level = score.risk_level
                row.explanation = score.explanation
                row.factors = list(score.factors or [])
                row.step_up_recommended = score.step_up_recommended
                row.user_id = score.user_id

    async def list_by_tenant(self, tenant_id: str) -> list[RiskScore]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(IdentityRiskScoreRow).where(IdentityRiskScoreRow.tenant_id == tenant_id)
                )
            ).all()
        return [_score_from_row(r) for r in rows]

    async def find_by_ref(self, tenant_id: str, score_ref: str) -> RiskScore | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(IdentityRiskScoreRow).where(
                    IdentityRiskScoreRow.tenant_id == tenant_id,
                    IdentityRiskScoreRow.score_ref == score_ref,
                )
            )
            return _score_from_row(row) if row else None

    def next_score_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "score")


class PostgresAnomalyAlertRepository(IAnomalyAlertRepository, _RefCounterMixin):
    async def save(self, alert: AnomalyAlert) -> None:
        async with session_scope(tenant_id=alert.tenant_id) as session:
            row = await session.get(IdentityRiskAlertRow, (alert.tenant_id, _uuid(alert.id)))
            if row is None:
                session.add(
                    IdentityRiskAlertRow(
                        tenant_id=alert.tenant_id,
                        id=_uuid(alert.id),
                        alert_ref=alert.alert_ref,
                        score_ref=alert.score_ref,
                        title=alert.title,
                        severity=alert.severity,
                        description=alert.description,
                        acknowledged=alert.acknowledged,
                        created_at=alert.created_at,
                    )
                )
            else:
                row.alert_ref = alert.alert_ref
                row.score_ref = alert.score_ref
                row.title = alert.title
                row.severity = alert.severity
                row.description = alert.description
                row.acknowledged = alert.acknowledged

    async def list_by_tenant(self, tenant_id: str) -> list[AnomalyAlert]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(IdentityRiskAlertRow).where(IdentityRiskAlertRow.tenant_id == tenant_id)
                )
            ).all()
        return [_alert_from_row(r) for r in rows]

    def next_alert_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "alert")
