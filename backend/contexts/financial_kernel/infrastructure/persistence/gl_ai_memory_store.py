"""In-memory General Ledger AI persistence."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.gl_ai import GLAIJob
from contexts.financial_kernel.domain.ports.gl_ai_repositories import IGLAIJobRepository


class InMemoryGLAIJobRepository(IGLAIJobRepository):
    _jobs: dict[str, GLAIJob] = {}

    @classmethod
    def reset(cls) -> None:
        cls._jobs = {}

    async def save(self, job: GLAIJob) -> None:
        self._jobs[str(job.id)] = job

    async def find_by_id(self, job_id: str) -> GLAIJob | None:
        return self._jobs.get(job_id)

    async def list_by_tenant(self, tenant_id: str) -> list[GLAIJob]:
        return [j for j in self._jobs.values() if j.tenant_id == tenant_id]

    async def list_by_capability(self, tenant_id: str, capability: str) -> list[GLAIJob]:
        return [j for j in await self.list_by_tenant(tenant_id) if j.capability == capability]
