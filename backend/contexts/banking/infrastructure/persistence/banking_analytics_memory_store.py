"""In-memory Banking Analytics repositories."""
from __future__ import annotations

from contexts.banking.domain.aggregates.banking_analytics_engine import BankingAnalyticsJob
from contexts.banking.domain.ports.banking_analytics_repositories import IBankingAnalyticsJobRepository


class InMemoryBankingAnalyticsJobRepository(IBankingAnalyticsJobRepository):
    _jobs: dict[str, BankingAnalyticsJob] = {}
    _refs: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls._jobs = {}
        cls._refs = {}

    async def save(self, job: BankingAnalyticsJob) -> None:
        self._jobs[str(job.id)] = job

    async def find_by_id(self, job_id: str) -> BankingAnalyticsJob | None:
        return self._jobs.get(job_id)

    async def list_by_tenant(self, tenant_id: str, capability: str | None = None) -> list[BankingAnalyticsJob]:
        jobs = [j for j in self._jobs.values() if j.tenant_id == tenant_id]
        if capability:
            jobs = [j for j in jobs if j.capability == capability]
        return sorted(jobs, key=lambda j: j.created_at, reverse=True)

    def next_job_ref(self, tenant_id: str) -> str:
        self._refs[tenant_id] = self._refs.get(tenant_id, 0) + 1
        return f"BAJ-{self._refs[tenant_id]:06d}"
