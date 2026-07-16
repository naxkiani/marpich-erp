"""Enterprise Scheduler engine."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.enterprise_scheduler.domain.aggregates.enterprise_scheduler_platform import (
    ExecutionStatus,
    JobStatus,
    JobType,
    SchedulerCapability,
)

POLICY_KEYS = [
    "enterprise_scheduler.cron.enabled",
    "enterprise_scheduler.calendar.enabled",
    "enterprise_scheduler.recurring.enabled",
    "enterprise_scheduler.event_trigger.enabled",
    "enterprise_scheduler.workflow_trigger.enabled",
    "enterprise_scheduler.retry.enabled",
    "enterprise_scheduler.priority.enabled",
    "enterprise_scheduler.distributed.enabled",
]

CAPABILITY_LABELS = {
    SchedulerCapability.CRON_JOBS.value: "Cron Jobs",
    SchedulerCapability.CALENDAR_JOBS.value: "Calendar Jobs",
    SchedulerCapability.RECURRING_JOBS.value: "Recurring Jobs",
    SchedulerCapability.EVENT_TRIGGERED_JOBS.value: "Event Triggered Jobs",
    SchedulerCapability.WORKFLOW_TRIGGERED_JOBS.value: "Workflow Triggered Jobs",
    SchedulerCapability.RETRY.value: "Retry",
    SchedulerCapability.PRIORITY.value: "Priority",
    SchedulerCapability.DEPENDENCY.value: "Dependency",
    SchedulerCapability.DISTRIBUTED_SCHEDULING.value: "Distributed Scheduling",
    SchedulerCapability.JOB_HISTORY.value: "Job History",
    SchedulerCapability.MONITORING.value: "Monitoring",
    SchedulerCapability.SCHEDULER_DASHBOARD.value: "Scheduler Dashboard",
}


def list_capability_catalog() -> list[dict]:
    return [
        {"capability": c.value, "label": CAPABILITY_LABELS.get(c.value, c.name.replace("_", " ").title())}
        for c in SchedulerCapability
    ]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def dependency_map() -> dict:
    return {
        "nodes": [
            {"id": "enterprise_scheduler", "type": "platform", "label": "Enterprise Scheduler"},
            {"id": "workflow", "type": "platform", "label": "Workflow"},
            {"id": "enterprise_message_orchestration", "type": "platform", "label": "Message Orchestration"},
            {"id": "enterprise_observability", "type": "platform", "label": "Observability"},
        ],
        "edges": [
            {"from": "enterprise_scheduler", "to": "workflow", "type": "workflow_trigger_delegate"},
            {"from": "enterprise_scheduler", "to": "enterprise_message_orchestration", "type": "delayed_queue_delegate"},
            {"from": "enterprise_scheduler", "to": "enterprise_observability", "type": "monitoring_delegate"},
        ],
        "distributed": True,
        "multi_tenant": True,
    }


def dependencies_satisfied(*, job: dict, dependencies: list[dict], executions: list[dict]) -> bool:
    deps = [d for d in dependencies if d.get("job_ref") == job.get("job_ref")]
    if not deps and not job.get("depends_on"):
        return True
    refs = {d.get("depends_on_job_ref") for d in deps} | set(job.get("depends_on", []))
    for ref in refs:
        if not ref:
            continue
        latest = next(
            (e for e in sorted(executions, key=lambda x: x.get("started_at", ""), reverse=True)
             if e.get("job_ref") == ref),
            None,
        )
        if not latest or latest.get("status") != ExecutionStatus.SUCCEEDED.value:
            return False
    return True


def resolve_worker_shard(*, job_ref: str, shard_count: int = 4) -> str:
    return f"shard-{hash(job_ref) % shard_count}"


def should_retry(*, retry_count: int, max_retries: int, retry_enabled: bool) -> bool:
    return retry_enabled and retry_count < max_retries


def build_monitoring(*, jobs: list[dict], executions: list[dict]) -> dict:
    total = len(executions)
    succeeded = len([e for e in executions if e.get("status") == ExecutionStatus.SUCCEEDED.value])
    failed = len([e for e in executions if e.get("status") == ExecutionStatus.FAILED.value])
    running = len([e for e in executions if e.get("status") == ExecutionStatus.RUNNING.value])
    by_type: dict[str, int] = {}
    for j in jobs:
        t = j.get("job_type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1
    by_shard: dict[str, int] = {}
    for j in jobs:
        s = j.get("worker_shard", "default")
        by_shard[s] = by_shard.get(s, 0) + 1
    return {
        "jobs_total": len(jobs),
        "executions_total": total,
        "succeeded": succeeded,
        "failed": failed,
        "running": running,
        "success_rate_pct": round((succeeded / total) * 100, 2) if total else 100.0,
        "jobs_by_type": by_type,
        "jobs_by_shard": by_shard,
        "paused_jobs": len([j for j in jobs if j.get("status") == JobStatus.PAUSED.value]),
    }


def build_dashboard(
    *,
    profile: dict | None,
    jobs: list[dict],
    executions: list[dict],
    dependencies: list[dict],
) -> dict:
    monitoring = build_monitoring(jobs=jobs, executions=executions)
    recent = sorted(executions, key=lambda e: e.get("started_at", ""), reverse=True)[:10]
    return {
        "summary": {
            "capabilities": len(SchedulerCapability),
            **monitoring,
            "dependencies": len(dependencies),
            "distributed_shards": len(monitoring["jobs_by_shard"]),
        },
        "profile": profile,
        "recent_executions": recent,
        "jobs_by_status": _count_by(jobs, "status"),
        "executions_by_status": _count_by(executions, "status"),
        "capabilities": list_capability_catalog(),
    }


def _count_by(items: list[dict], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        key = str(item.get(field, "unknown"))
        counts[key] = counts.get(key, 0) + 1
    return counts


def generate_seed_data() -> dict:
    now = datetime.now(UTC)
    return {
        "jobs": [
            {
                "name": "Nightly GL Close",
                "job_type": JobType.CRON.value,
                "cron_expression": "0 2 * * *",
                "priority": 9,
                "worker_shard": "shard-0",
            },
            {
                "name": "Month-End Calendar Close",
                "job_type": JobType.CALENDAR.value,
                "calendar_rule": "last_business_day_of_month",
                "priority": 10,
                "worker_shard": "shard-1",
            },
            {
                "name": "Hourly Sync Recurring",
                "job_type": JobType.RECURRING.value,
                "recurrence_rule": "every 1 hour",
                "priority": 5,
                "worker_shard": "shard-2",
            },
            {
                "name": "On User Created",
                "job_type": JobType.EVENT.value,
                "event_pattern": "identity.user.created",
                "priority": 7,
                "worker_shard": "shard-0",
            },
            {
                "name": "Post-Approval Workflow",
                "job_type": JobType.WORKFLOW.value,
                "workflow_ref": "WF-APPROVAL-POST",
                "priority": 8,
                "depends_on": [],
                "worker_shard": "shard-3",
            },
        ],
        "dependencies": [
            {"job_index": 4, "depends_on_index": 0},
        ],
        "executions": [
            {"job_index": 0, "status": ExecutionStatus.SUCCEEDED.value, "duration_ms": 1250.0, "attempt": 1},
            {"job_index": 0, "status": ExecutionStatus.SUCCEEDED.value, "duration_ms": 1180.0, "attempt": 1},
            {"job_index": 2, "status": ExecutionStatus.FAILED.value, "duration_ms": 320.0, "attempt": 1, "error": "timeout"},
            {"job_index": 2, "status": ExecutionStatus.SUCCEEDED.value, "duration_ms": 890.0, "attempt": 2},
            {"job_index": 3, "status": ExecutionStatus.SUCCEEDED.value, "duration_ms": 45.0, "attempt": 1},
        ],
        "next_run_offset_minutes": 30,
        "seeded_at": now.isoformat(),
    }
