"""In-memory identity risk persistence."""
from __future__ import annotations

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


class InMemoryIdentityRiskStore:
    profiles: dict[str, RiskProfile] = {}
    signals: dict[str, RiskSignal] = {}
    scores: dict[str, RiskScore] = {}
    alerts: dict[str, AnomalyAlert] = {}
    profile_counter: dict[str, int] = {}
    signal_counter: dict[str, int] = {}
    score_counter: dict[str, int] = {}
    alert_counter: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls.profiles.clear()
        cls.signals.clear()
        cls.scores.clear()
        cls.alerts.clear()
        cls.profile_counter.clear()
        cls.signal_counter.clear()
        cls.score_counter.clear()
        cls.alert_counter.clear()


class InMemoryRiskProfileRepository(IRiskProfileRepository):
    async def find_by_tenant(self, tenant_id: str) -> RiskProfile | None:
        return InMemoryIdentityRiskStore.profiles.get(tenant_id)

    async def save(self, profile: RiskProfile) -> None:
        InMemoryIdentityRiskStore.profiles[profile.tenant_id] = profile

    def next_profile_ref(self, tenant_id: str) -> str:
        n = InMemoryIdentityRiskStore.profile_counter.get(tenant_id, 0) + 1
        InMemoryIdentityRiskStore.profile_counter[tenant_id] = n
        return f"risk-profile-{tenant_id}-{n:04d}"


class InMemoryRiskSignalRepository(IRiskSignalRepository):
    async def save(self, signal: RiskSignal) -> None:
        InMemoryIdentityRiskStore.signals[signal.signal_ref] = signal

    async def list_by_tenant(self, tenant_id: str) -> list[RiskSignal]:
        return [s for s in InMemoryIdentityRiskStore.signals.values() if s.tenant_id == tenant_id]

    def next_signal_ref(self, tenant_id: str) -> str:
        n = InMemoryIdentityRiskStore.signal_counter.get(tenant_id, 0) + 1
        InMemoryIdentityRiskStore.signal_counter[tenant_id] = n
        return f"signal-{tenant_id}-{n:04d}"


class InMemoryRiskScoreRepository(IRiskScoreRepository):
    async def save(self, score: RiskScore) -> None:
        InMemoryIdentityRiskStore.scores[score.score_ref] = score

    async def list_by_tenant(self, tenant_id: str) -> list[RiskScore]:
        return [s for s in InMemoryIdentityRiskStore.scores.values() if s.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, score_ref: str) -> RiskScore | None:
        score = InMemoryIdentityRiskStore.scores.get(score_ref)
        if score and score.tenant_id == tenant_id:
            return score
        return None

    def next_score_ref(self, tenant_id: str) -> str:
        n = InMemoryIdentityRiskStore.score_counter.get(tenant_id, 0) + 1
        InMemoryIdentityRiskStore.score_counter[tenant_id] = n
        return f"score-{tenant_id}-{n:04d}"


class InMemoryAnomalyAlertRepository(IAnomalyAlertRepository):
    async def save(self, alert: AnomalyAlert) -> None:
        InMemoryIdentityRiskStore.alerts[alert.alert_ref] = alert

    async def list_by_tenant(self, tenant_id: str) -> list[AnomalyAlert]:
        return [a for a in InMemoryIdentityRiskStore.alerts.values() if a.tenant_id == tenant_id]

    def next_alert_ref(self, tenant_id: str) -> str:
        n = InMemoryIdentityRiskStore.alert_counter.get(tenant_id, 0) + 1
        InMemoryIdentityRiskStore.alert_counter[tenant_id] = n
        return f"alert-{tenant_id}-{n:04d}"
