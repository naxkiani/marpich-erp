"""Enterprise Business Continuity Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ContinuityCapability(StrEnum):
    DISASTER_RECOVERY = "disaster_recovery"
    BUSINESS_CONTINUITY_PLAN = "business_continuity_plan"
    BACKUP_STRATEGY = "backup_strategy"
    RECOVERY_POINT_OBJECTIVE = "recovery_point_objective"
    RECOVERY_TIME_OBJECTIVE = "recovery_time_objective"
    FAILOVER = "failover"
    HIGH_AVAILABILITY = "high_availability"
    REPLICATION = "replication"
    EMERGENCY_OPERATIONS = "emergency_operations"
    RECOVERY_TESTING = "recovery_testing"
    CONTINUITY_DASHBOARD = "continuity_dashboard"


class PlanType(StrEnum):
    BCP = "bcp"
    DR = "dr"
    EMERGENCY_OPS = "emergency_ops"


class PlanStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    TESTING = "testing"
    RETIRED = "retired"


class FailoverStatus(StrEnum):
    STANDBY = "standby"
    INITIATED = "initiated"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class TestStatus(StrEnum):
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"


class CriticalityTier(StrEnum):
    TIER_1 = "tier_1"
    TIER_2 = "tier_2"
    TIER_3 = "tier_3"


@dataclass(eq=False, kw_only=True)
class ContinuityTenantProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    default_rpo_hours: int = 4
    default_rto_hours: int = 8
    ha_enabled: bool = True
    replication_enabled: bool = True
    auto_failover: bool = False
    test_frequency_days: int = 90
    enabled_tiers: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        profile_ref: str,
        enabled_tiers: list[str],
        metadata: dict | None = None,
    ) -> ContinuityTenantProfile:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            profile_ref=profile_ref,
            enabled_tiers=enabled_tiers,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "default_rpo_hours": self.default_rpo_hours,
            "default_rto_hours": self.default_rto_hours,
            "ha_enabled": self.ha_enabled,
            "replication_enabled": self.replication_enabled,
            "auto_failover": self.auto_failover,
            "test_frequency_days": self.test_frequency_days,
            "enabled_tiers": self.enabled_tiers,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class ContinuityPlan(AggregateRoot):
    tenant_id: str
    plan_ref: str
    title: str
    plan_type: str
    criticality_tier: str
    rpo_hours: int
    rto_hours: int
    status: str
    owner_id: str = ""
    recovery_steps: list[str] = field(default_factory=list)
    delegated_to: str | None = None
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        plan_ref: str,
        title: str,
        plan_type: str,
        criticality_tier: str,
        rpo_hours: int,
        rto_hours: int,
        owner_id: str = "",
        recovery_steps: list[str] | None = None,
        delegated_to: str | None = None,
        metadata: dict | None = None,
    ) -> ContinuityPlan:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            plan_ref=plan_ref,
            title=title,
            plan_type=plan_type,
            criticality_tier=criticality_tier,
            rpo_hours=rpo_hours,
            rto_hours=rto_hours,
            status=PlanStatus.ACTIVE.value,
            owner_id=owner_id,
            recovery_steps=recovery_steps or [],
            delegated_to=delegated_to,
            metadata=metadata or {},
        )

    def activate(self) -> None:
        self.status = PlanStatus.ACTIVE.value
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "plan_ref": self.plan_ref,
            "tenant_id": self.tenant_id,
            "title": self.title,
            "plan_type": self.plan_type,
            "criticality_tier": self.criticality_tier,
            "rpo_hours": self.rpo_hours,
            "rto_hours": self.rto_hours,
            "status": self.status,
            "owner_id": self.owner_id,
            "recovery_steps": self.recovery_steps,
            "delegated_to": self.delegated_to,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BackupStrategy(AggregateRoot):
    tenant_id: str
    strategy_ref: str
    name: str
    backup_type: str
    frequency_hours: int
    retention_days: int
    rpo_hours: int
    encrypted: bool = True
    delegated_to: str | None = "data_protection"
    status: str = PlanStatus.ACTIVE.value
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        strategy_ref: str,
        name: str,
        backup_type: str,
        frequency_hours: int,
        retention_days: int,
        rpo_hours: int,
        encrypted: bool = True,
        metadata: dict | None = None,
    ) -> BackupStrategy:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            strategy_ref=strategy_ref,
            name=name,
            backup_type=backup_type,
            frequency_hours=frequency_hours,
            retention_days=retention_days,
            rpo_hours=rpo_hours,
            encrypted=encrypted,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "strategy_ref": self.strategy_ref,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "backup_type": self.backup_type,
            "frequency_hours": self.frequency_hours,
            "retention_days": self.retention_days,
            "rpo_hours": self.rpo_hours,
            "encrypted": self.encrypted,
            "delegated_to": self.delegated_to,
            "status": self.status,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class FailoverRecord(AggregateRoot):
    tenant_id: str
    failover_ref: str
    source_system: str
    target_system: str
    status: str
    trigger_reason: str = ""
    rto_target_hours: int = 8
    initiated_by: str = ""
    completed_at: str | None = None
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def initiate(
        cls,
        *,
        tenant_id: str,
        failover_ref: str,
        source_system: str,
        target_system: str,
        trigger_reason: str,
        rto_target_hours: int,
        initiated_by: str = "",
        metadata: dict | None = None,
    ) -> FailoverRecord:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            failover_ref=failover_ref,
            source_system=source_system,
            target_system=target_system,
            status=FailoverStatus.INITIATED.value,
            trigger_reason=trigger_reason,
            rto_target_hours=rto_target_hours,
            initiated_by=initiated_by,
            metadata=metadata or {},
        )

    def complete(self) -> None:
        self.status = FailoverStatus.COMPLETED.value
        self.completed_at = datetime.now(UTC).isoformat()

    def fail(self) -> None:
        self.status = FailoverStatus.FAILED.value
        self.completed_at = datetime.now(UTC).isoformat()

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "failover_ref": self.failover_ref,
            "tenant_id": self.tenant_id,
            "source_system": self.source_system,
            "target_system": self.target_system,
            "status": self.status,
            "trigger_reason": self.trigger_reason,
            "rto_target_hours": self.rto_target_hours,
            "initiated_by": self.initiated_by,
            "completed_at": self.completed_at,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class RecoveryTest(AggregateRoot):
    tenant_id: str
    test_ref: str
    plan_ref: str
    test_type: str
    status: str
    rto_achieved_hours: float | None = None
    rpo_achieved_hours: float | None = None
    passed: bool = False
    findings: list[str] = field(default_factory=list)
    executed_by: str = ""
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def schedule(
        cls,
        *,
        tenant_id: str,
        test_ref: str,
        plan_ref: str,
        test_type: str,
        executed_by: str = "",
        metadata: dict | None = None,
    ) -> RecoveryTest:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            test_ref=test_ref,
            plan_ref=plan_ref,
            test_type=test_type,
            status=TestStatus.SCHEDULED.value,
            executed_by=executed_by,
            metadata=metadata or {},
        )

    def run(self, *, rto_achieved: float, rpo_achieved: float, rto_target: int, rpo_target: int) -> None:
        self.status = TestStatus.RUNNING.value
        self.rto_achieved_hours = rto_achieved
        self.rpo_achieved_hours = rpo_achieved
        self.passed = rto_achieved <= rto_target and rpo_achieved <= rpo_target
        self.status = TestStatus.PASSED.value if self.passed else TestStatus.FAILED.value
        if not self.passed:
            if rto_achieved > rto_target:
                self.findings.append(f"RTO exceeded: {rto_achieved}h > {rto_target}h target")
            if rpo_achieved > rpo_target:
                self.findings.append(f"RPO exceeded: {rpo_achieved}h > {rpo_target}h target")

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "test_ref": self.test_ref,
            "tenant_id": self.tenant_id,
            "plan_ref": self.plan_ref,
            "test_type": self.test_type,
            "status": self.status,
            "rto_achieved_hours": self.rto_achieved_hours,
            "rpo_achieved_hours": self.rpo_achieved_hours,
            "passed": self.passed,
            "findings": self.findings,
            "executed_by": self.executed_by,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }
