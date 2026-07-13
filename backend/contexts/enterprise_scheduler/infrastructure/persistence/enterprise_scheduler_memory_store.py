"""In-memory Enterprise Scheduler persistence."""
from __future__ import annotations

from contexts.enterprise_scheduler.domain.aggregates.enterprise_scheduler_platform import (
    JobDependency,
    JobExecution,
    ScheduledJob,
    SchedulerProfile,
)
from contexts.enterprise_scheduler.domain.ports.enterprise_scheduler_repositories import (
    IJobDependencyRepository,
    IJobExecutionRepository,
    IScheduledJobRepository,
    ISchedulerProfileRepository,
)


class _RefCounter:
    _counters: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls._counters = {}

    @classmethod
    def next(cls, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        n = cls._counters.get(key, 0) + 1
        cls._counters[key] = n
        return f"{prefix}-{tenant_id[:4].upper()}-{n:05d}"


class InMemorySchedulerProfileRepository(ISchedulerProfileRepository):
    _store: dict[str, SchedulerProfile] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, profile: SchedulerProfile) -> None:
        self._store[str(profile.id)] = profile

    async def find_by_tenant(self, tenant_id: str) -> SchedulerProfile | None:
        for p in self._store.values():
            if p.tenant_id == tenant_id:
                return p
        return None

    def next_profile_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-SCH-PRF")


class InMemoryScheduledJobRepository(IScheduledJobRepository):
    _store: dict[str, ScheduledJob] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, job: ScheduledJob) -> None:
        self._store[str(job.id)] = job

    async def list_by_tenant(self, tenant_id: str) -> list[ScheduledJob]:
        return [j for j in self._store.values() if j.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, job_ref: str) -> ScheduledJob | None:
        for j in self._store.values():
            if j.tenant_id == tenant_id and j.job_ref == job_ref:
                return j
        return None

    def next_job_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-SCH-JOB")


class InMemoryJobDependencyRepository(IJobDependencyRepository):
    _store: dict[str, JobDependency] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, dependency: JobDependency) -> None:
        self._store[str(dependency.id)] = dependency

    async def list_by_tenant(self, tenant_id: str) -> list[JobDependency]:
        return [d for d in self._store.values() if d.tenant_id == tenant_id]

    def next_dependency_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-SCH-DEP")


class InMemoryJobExecutionRepository(IJobExecutionRepository):
    _store: dict[str, JobExecution] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, execution: JobExecution) -> None:
        self._store[str(execution.id)] = execution

    async def list_by_tenant(self, tenant_id: str) -> list[JobExecution]:
        return sorted(
            [e for e in self._store.values() if e.tenant_id == tenant_id],
            key=lambda e: e.started_at,
            reverse=True,
        )

    async def list_by_job(self, tenant_id: str, job_ref: str) -> list[JobExecution]:
        return [e for e in await self.list_by_tenant(tenant_id) if e.job_ref == job_ref]

    def next_execution_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-SCH-EX")
