"""Enterprise Scheduler — unit tests."""
import pytest

from contexts.enterprise_scheduler.domain.aggregates.enterprise_scheduler_platform import SchedulerCapability
from contexts.enterprise_scheduler.domain.services import enterprise_scheduler_engine as engine


@pytest.mark.unit
def test_capability_catalog_has_twelve_capabilities():
    caps = {c["capability"] for c in engine.list_capability_catalog()}
    assert SchedulerCapability.CRON_JOBS.value in caps
    assert SchedulerCapability.SCHEDULER_DASHBOARD.value in caps
    assert len(caps) == 12


@pytest.mark.unit
def test_dependencies_satisfied():
    job = {"job_ref": "B", "depends_on": ["A"]}
    deps = [{"job_ref": "B", "depends_on_job_ref": "A"}]
    execs = [{"job_ref": "A", "status": "succeeded", "started_at": "2026-01-01"}]
    assert engine.dependencies_satisfied(job=job, dependencies=deps, executions=execs) is True


@pytest.mark.unit
def test_should_retry():
    assert engine.should_retry(retry_count=1, max_retries=3, retry_enabled=True) is True
    assert engine.should_retry(retry_count=3, max_retries=3, retry_enabled=True) is False


@pytest.mark.unit
def test_build_dashboard_structure():
    jobs = [{"job_ref": "J1", "job_type": "cron", "status": "scheduled", "worker_shard": "shard-0"}]
    execs = [{"job_ref": "J1", "status": "succeeded", "started_at": "2026-01-02"}]
    dash = engine.build_dashboard(profile=None, jobs=jobs, executions=execs, dependencies=[])
    assert dash["summary"]["capabilities"] == 12
    assert dash["summary"]["jobs_total"] == 1
