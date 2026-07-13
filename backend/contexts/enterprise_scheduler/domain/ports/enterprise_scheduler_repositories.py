"""Enterprise Scheduler repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.enterprise_scheduler.domain.aggregates.enterprise_scheduler_platform import (
    JobDependency,
    JobExecution,
    ScheduledJob,
    SchedulerProfile,
)


class ISchedulerProfileRepository(ABC):
    @abstractmethod
    async def save(self, profile: SchedulerProfile) -> None: ...

    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> SchedulerProfile | None: ...

    @abstractmethod
    def next_profile_ref(self, tenant_id: str) -> str: ...


class IScheduledJobRepository(ABC):
    @abstractmethod
    async def save(self, job: ScheduledJob) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[ScheduledJob]: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, job_ref: str) -> ScheduledJob | None: ...

    @abstractmethod
    def next_job_ref(self, tenant_id: str) -> str: ...


class IJobDependencyRepository(ABC):
    @abstractmethod
    async def save(self, dependency: JobDependency) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[JobDependency]: ...

    @abstractmethod
    def next_dependency_ref(self, tenant_id: str) -> str: ...


class IJobExecutionRepository(ABC):
    @abstractmethod
    async def save(self, execution: JobExecution) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[JobExecution]: ...

    @abstractmethod
    async def list_by_job(self, tenant_id: str, job_ref: str) -> list[JobExecution]: ...

    @abstractmethod
    def next_execution_ref(self, tenant_id: str) -> str: ...
