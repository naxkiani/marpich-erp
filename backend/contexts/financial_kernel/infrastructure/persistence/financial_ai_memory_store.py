"""In-memory Financial AI persistence."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.financial_ai import (
    FinancialAIChatSession,
    FinancialAIJob,
)
from contexts.financial_kernel.domain.ports.financial_ai_repositories import (
    IFinancialAIChatRepository,
    IFinancialAIJobRepository,
)


class InMemoryFinancialAIJobRepository(IFinancialAIJobRepository):
    _jobs: dict[str, FinancialAIJob] = {}

    @classmethod
    def reset(cls) -> None:
        cls._jobs = {}

    async def save(self, job: FinancialAIJob) -> None:
        self._jobs[str(job.id)] = job

    async def find_by_id(self, job_id: str) -> FinancialAIJob | None:
        return self._jobs.get(job_id)

    async def list_by_tenant(self, tenant_id: str) -> list[FinancialAIJob]:
        return [j for j in self._jobs.values() if j.tenant_id == tenant_id]

    async def list_by_capability(self, tenant_id: str, capability: str) -> list[FinancialAIJob]:
        return [j for j in await self.list_by_tenant(tenant_id) if j.capability == capability]


class InMemoryFinancialAIChatRepository(IFinancialAIChatRepository):
    _sessions: dict[str, FinancialAIChatSession] = {}

    @classmethod
    def reset(cls) -> None:
        cls._sessions = {}

    async def save(self, session: FinancialAIChatSession) -> None:
        self._sessions[str(session.id)] = session

    async def find_by_id(self, session_id: str) -> FinancialAIChatSession | None:
        return self._sessions.get(session_id)

    async def list_by_tenant(self, tenant_id: str) -> list[FinancialAIChatSession]:
        return [s for s in self._sessions.values() if s.tenant_id == tenant_id]
