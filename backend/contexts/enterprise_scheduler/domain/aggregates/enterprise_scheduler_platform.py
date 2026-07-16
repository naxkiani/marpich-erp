"""Enterprise Scheduler Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class SchedulerCapability(StrEnum):
    CRON_JOBS = "cron_jobs"
    CALENDAR_JOBS = "calendar_jobs"
    RECURRING_JOBS = "recurring_jobs"
    EVENT_TRIGGERED_JOBS = "event_triggered_jobs"
    WORKFLOW_TRIGGERED_JOBS = "workflow_triggered_jobs"
    RETRY = "retry"
    PRIORITY = "priority"
    DEPENDENCY = "dependency"
    DISTRIBUTED_SCHEDULING = "distributed_scheduling"
    JOB_HISTORY = "job_history"
    MONITORING = "monitoring"
    SCHEDULER_DASHBOARD = "scheduler_dashboard"


class JobType(StrEnum):
    CRON = "cron"
    CALENDAR = "calendar"
    RECURRING = "recurring"
    EVENT = "event"
    WORKFLOW = "workflow"


class JobStatus(StrEnum):
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExecutionStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    RETRYING = "retrying"
    SKIPPED = "skipped"


@dataclass(eq=False, kw_only=True)
class SchedulerProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    cron_enabled: bool = True
    calendar_enabled: bool = True
    recurring_enabled: bool = True
    event_trigger_enabled: bool = True
    workflow_trigger_enabled: bool = True
    retry_enabled: bool = True
    priority_enabled: bool = True
    distributed_enabled: bool = True
    max_retries: int = 3
    default_priority: int = 5
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str) -> SchedulerProfile:
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, profile_ref=profile_ref)

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "cron_enabled": self.cron_enabled,
            "calendar_enabled": self.calendar_enabled,
            "recurring_enabled": self.recurring_enabled,
            "event_trigger_enabled": self.event_trigger_enabled,
            "workflow_trigger_enabled": self.workflow_trigger_enabled,
            "retry_enabled": self.retry_enabled,
            "priority_enabled": self.priority_enabled,
            "distributed_enabled": self.distributed_enabled,
            "max_retries": self.max_retries,
            "default_priority": self.default_priority,
        }


@dataclass(eq=False, kw_only=True)
class ScheduledJob(AggregateRoot):
    tenant_id: str
    job_ref: str
    name: str
    job_type: str
    status: str
    cron_expression: str = ""
    calendar_rule: str = ""
    recurrence_rule: str = ""
    event_pattern: str = ""
    workflow_ref: str = ""
    priority: int = 5
    max_retries: int = 3
    retry_count: int = 0
    depends_on: list[str] = field(default_factory=list)
    worker_shard: str = "default"
    payload: dict = field(default_factory=dict)
    next_run_at: datetime | None = None
    last_run_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        job_ref: str,
        name: str,
        job_type: str,
        cron_expression: str = "",
        calendar_rule: str = "",
        recurrence_rule: str = "",
        event_pattern: str = "",
        workflow_ref: str = "",
        priority: int = 5,
        max_retries: int = 3,
        depends_on: list[str] | None = None,
        worker_shard: str = "default",
        payload: dict | None = None,
    ) -> ScheduledJob:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            job_ref=job_ref,
            name=name,
            job_type=job_type,
            status=JobStatus.SCHEDULED.value,
            cron_expression=cron_expression,
            calendar_rule=calendar_rule,
            recurrence_rule=recurrence_rule,
            event_pattern=event_pattern,
            workflow_ref=workflow_ref,
            priority=priority,
            max_retries=max_retries,
            depends_on=depends_on or [],
            worker_shard=worker_shard,
            payload=payload or {},
        )

    def pause(self) -> None:
        self.status = JobStatus.PAUSED.value

    def resume(self) -> None:
        self.status = JobStatus.SCHEDULED.value

    def to_dict(self) -> dict:
        return {
            "job_ref": self.job_ref,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "job_type": self.job_type,
            "status": self.status,
            "cron_expression": self.cron_expression,
            "calendar_rule": self.calendar_rule,
            "recurrence_rule": self.recurrence_rule,
            "event_pattern": self.event_pattern,
            "workflow_ref": self.workflow_ref,
            "priority": self.priority,
            "max_retries": self.max_retries,
            "retry_count": self.retry_count,
            "depends_on": self.depends_on,
            "worker_shard": self.worker_shard,
            "payload": self.payload,
            "next_run_at": self.next_run_at.isoformat() if self.next_run_at else None,
            "last_run_at": self.last_run_at.isoformat() if self.last_run_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class JobDependency(AggregateRoot):
    tenant_id: str
    dependency_ref: str
    job_ref: str
    depends_on_job_ref: str
    required_status: str = ExecutionStatus.SUCCEEDED.value
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def link(
        cls,
        *,
        tenant_id: str,
        dependency_ref: str,
        job_ref: str,
        depends_on_job_ref: str,
        required_status: str = ExecutionStatus.SUCCEEDED.value,
    ) -> JobDependency:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            dependency_ref=dependency_ref,
            job_ref=job_ref,
            depends_on_job_ref=depends_on_job_ref,
            required_status=required_status,
        )

    def to_dict(self) -> dict:
        return {
            "dependency_ref": self.dependency_ref,
            "job_ref": self.job_ref,
            "depends_on_job_ref": self.depends_on_job_ref,
            "required_status": self.required_status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class JobExecution(AggregateRoot):
    tenant_id: str
    execution_ref: str
    job_ref: str
    status: str
    attempt: int = 1
    worker_shard: str = "default"
    duration_ms: float = 0.0
    error_message: str = ""
    correlation_id: str = ""
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def start(
        cls,
        *,
        tenant_id: str,
        execution_ref: str,
        job_ref: str,
        attempt: int = 1,
        worker_shard: str = "default",
        correlation_id: str = "",
    ) -> JobExecution:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            execution_ref=execution_ref,
            job_ref=job_ref,
            status=ExecutionStatus.RUNNING.value,
            attempt=attempt,
            worker_shard=worker_shard,
            correlation_id=correlation_id,
        )

    def complete(self, *, duration_ms: float) -> None:
        self.status = ExecutionStatus.SUCCEEDED.value
        self.duration_ms = duration_ms
        self.completed_at = datetime.now(UTC)

    def fail(self, *, error_message: str, duration_ms: float = 0) -> None:
        self.status = ExecutionStatus.FAILED.value
        self.error_message = error_message
        self.duration_ms = duration_ms
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "execution_ref": self.execution_ref,
            "job_ref": self.job_ref,
            "status": self.status,
            "attempt": self.attempt,
            "worker_shard": self.worker_shard,
            "duration_ms": self.duration_ms,
            "error_message": self.error_message,
            "correlation_id": self.correlation_id,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
