"""Delegates to directory and identity_risk workers."""
from __future__ import annotations

from contexts.directory.container import get_directory_service
from contexts.identity_resilience.domain.ports.identity_resilience_repositories import (
    IDirectoryWorkerPort,
    IRiskWorkerPort,
)


class DirectoryWorkerAdapter(IDirectoryWorkerPort):
    async def run_sync_worker(self, tenant_id: str) -> dict:
        result = await get_directory_service().run_sync_worker(tenant_id)
        if not result.succeeded:
            return {"processed": 0, "completed": 0, "failed": 0, "error": result.error}
        return result.unwrap()


class RiskWorkerAdapter(IRiskWorkerPort):
    async def process_pending_scores(self, tenant_id: str) -> dict:
        from contexts.identity_risk.container import get_identity_risk_service

        scores = await get_identity_risk_service().list_scores(tenant_id)
        count = len(scores.unwrap()) if scores.succeeded else 0
        return {"ready": True, "scores_recorded": count}
