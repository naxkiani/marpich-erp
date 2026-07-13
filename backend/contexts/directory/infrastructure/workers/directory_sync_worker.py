"""Directory sync worker — processes pending LDAP sync jobs."""
from __future__ import annotations

from contexts.directory.domain.aggregates.directory_platform import DirectorySyncJob


class DirectorySyncWorker:
    async def process_job(
        self,
        job: DirectorySyncJob,
        *,
        sync_fn,
    ) -> DirectorySyncJob:
        job.mark_running()
        try:
            result = await sync_fn(job.source_ref)
            job.mark_completed(synced=result["synced"], created=result["created"])
        except Exception as exc:  # noqa: BLE001 — worker boundary
            job.mark_failed(str(exc))
        return job
