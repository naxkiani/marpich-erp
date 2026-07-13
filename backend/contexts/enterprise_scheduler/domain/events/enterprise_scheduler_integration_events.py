"""Enterprise Scheduler integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class JobScheduledIntegration(IntegrationEvent):
    job_ref: str
    job_type: str
    next_run_at: str

    @property
    def event_name(self) -> str:
        return "enterprise_scheduler.job.scheduled"

    @property
    def source_context(self) -> str:
        return "enterprise_scheduler"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"job_ref": self.job_ref, "job_type": self.job_type, "next_run_at": self.next_run_at}


@dataclass(frozen=True, kw_only=True)
class JobStartedIntegration(IntegrationEvent):
    job_ref: str
    execution_ref: str
    worker_shard: str

    @property
    def event_name(self) -> str:
        return "enterprise_scheduler.job.started"

    @property
    def source_context(self) -> str:
        return "enterprise_scheduler"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "job_ref": self.job_ref,
            "execution_ref": self.execution_ref,
            "worker_shard": self.worker_shard,
        }


@dataclass(frozen=True, kw_only=True)
class JobCompletedIntegration(IntegrationEvent):
    job_ref: str
    execution_ref: str
    duration_ms: float

    @property
    def event_name(self) -> str:
        return "enterprise_scheduler.job.completed"

    @property
    def source_context(self) -> str:
        return "enterprise_scheduler"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "job_ref": self.job_ref,
            "execution_ref": self.execution_ref,
            "duration_ms": self.duration_ms,
        }


@dataclass(frozen=True, kw_only=True)
class JobFailedIntegration(IntegrationEvent):
    job_ref: str
    execution_ref: str
    error_message: str
    will_retry: bool

    @property
    def event_name(self) -> str:
        return "enterprise_scheduler.job.failed"

    @property
    def source_context(self) -> str:
        return "enterprise_scheduler"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "job_ref": self.job_ref,
            "execution_ref": self.execution_ref,
            "error_message": self.error_message,
            "will_retry": self.will_retry,
        }


@dataclass(frozen=True, kw_only=True)
class SchedulerDashboardGeneratedIntegration(IntegrationEvent):
    jobs_total: int
    executions_total: int
    success_rate_pct: float

    @property
    def event_name(self) -> str:
        return "enterprise_scheduler.dashboard.generated"

    @property
    def source_context(self) -> str:
        return "enterprise_scheduler"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "jobs_total": self.jobs_total,
            "executions_total": self.executions_total,
            "success_rate_pct": self.success_rate_pct,
        }
