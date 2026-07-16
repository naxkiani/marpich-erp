"""Enterprise Scheduler application service."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from contexts.enterprise_scheduler.domain.aggregates.enterprise_scheduler_platform import (
    ExecutionStatus,
    JobDependency,
    JobExecution,
    JobStatus,
    ScheduledJob,
    SchedulerProfile,
)
from contexts.enterprise_scheduler.domain.events.enterprise_scheduler_integration_events import (
    JobCompletedIntegration,
    JobFailedIntegration,
    JobScheduledIntegration,
    JobStartedIntegration,
    SchedulerDashboardGeneratedIntegration,
)
from contexts.enterprise_scheduler.domain.ports.enterprise_scheduler_repositories import (
    IJobDependencyRepository,
    IJobExecutionRepository,
    IScheduledJobRepository,
    ISchedulerProfileRepository,
)
from contexts.enterprise_scheduler.domain.services import enterprise_scheduler_engine as engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class EnterpriseSchedulerApplicationService:
    def __init__(
        self,
        profiles: ISchedulerProfileRepository,
        jobs: IScheduledJobRepository,
        dependencies: IJobDependencyRepository,
        executions: IJobExecutionRepository,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._jobs = jobs
        self._dependencies = dependencies
        self._executions = executions
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "cron_enabled": profile.cron_enabled if profile else True,
            "calendar_enabled": profile.calendar_enabled if profile else True,
            "recurring_enabled": profile.recurring_enabled if profile else True,
            "event_trigger_enabled": profile.event_trigger_enabled if profile else True,
            "workflow_trigger_enabled": profile.workflow_trigger_enabled if profile else True,
            "retry_enabled": profile.retry_enabled if profile else True,
            "priority_enabled": profile.priority_enabled if profile else True,
            "distributed_enabled": profile.distributed_enabled if profile else True,
            "max_retries": profile.max_retries if profile else 3,
            "default_priority": profile.default_priority if profile else 5,
        }
        pmap = {
            "enterprise_scheduler.cron.enabled": ("cron_enabled", "enabled"),
            "enterprise_scheduler.calendar.enabled": ("calendar_enabled", "enabled"),
            "enterprise_scheduler.recurring.enabled": ("recurring_enabled", "enabled"),
            "enterprise_scheduler.event_trigger.enabled": ("event_trigger_enabled", "enabled"),
            "enterprise_scheduler.workflow_trigger.enabled": ("workflow_trigger_enabled", "enabled"),
            "enterprise_scheduler.retry.enabled": ("retry_enabled", "enabled"),
            "enterprise_scheduler.priority.enabled": ("priority_enabled", "enabled"),
            "enterprise_scheduler.distributed.enabled": ("distributed_enabled", "enabled"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> SchedulerProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = SchedulerProfile.create(
            tenant_id=tenant_id,
            profile_ref=self._profiles.next_profile_ref(tenant_id),
        )
        await self._profiles.save(profile)
        return profile

    async def handle_tenant_provisioned(self, event: dict) -> None:
        tenant_id = event.get("tenant_id") or event.get("payload", {}).get("tenant_id")
        if tenant_id:
            await self.seed(tenant_id)

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": engine.list_capability_catalog(),
            "policy_keys": engine.list_policy_keys(),
            "job_types": ["cron", "calendar", "recurring", "event", "workflow"],
            "delegation": {
                "workflow_triggers": "workflow",
                "delayed_dispatch": "enterprise_message_orchestration",
                "monitoring": "enterprise_observability",
                "local_cron_duplication": False,
            },
        })

    async def get_dependency_map(self) -> Result[dict]:
        return Result.ok(engine.dependency_map())

    async def seed(self, tenant_id: str) -> Result[dict]:
        await self._ensure_profile(tenant_id)
        seed_data = engine.generate_seed_data()
        created_jobs: list[ScheduledJob] = []
        for jdata in seed_data["jobs"]:
            job = ScheduledJob.define(
                tenant_id=tenant_id,
                job_ref=self._jobs.next_job_ref(tenant_id),
                name=jdata["name"],
                job_type=jdata["job_type"],
                cron_expression=jdata.get("cron_expression", ""),
                calendar_rule=jdata.get("calendar_rule", ""),
                recurrence_rule=jdata.get("recurrence_rule", ""),
                event_pattern=jdata.get("event_pattern", ""),
                workflow_ref=jdata.get("workflow_ref", ""),
                priority=jdata.get("priority", 5),
                depends_on=jdata.get("depends_on", []),
                worker_shard=jdata.get("worker_shard", engine.resolve_worker_shard(job_ref="seed")),
            )
            job.next_run_at = datetime.now(UTC) + timedelta(minutes=seed_data.get("next_run_offset_minutes", 30))
            await self._jobs.save(job)
            created_jobs.append(job)
            await publish_integration_event(
                JobScheduledIntegration(
                    tenant_id=TenantId(tenant_id),
                    correlation_id=str(uuid.uuid4()),
                    job_ref=job.job_ref,
                    job_type=job.job_type,
                    next_run_at=job.next_run_at.isoformat() if job.next_run_at else "",
                )
            )

        dep_count = 0
        for ddata in seed_data["dependencies"]:
            job = created_jobs[ddata["job_index"]]
            parent = created_jobs[ddata["depends_on_index"]]
            dep = JobDependency.link(
                tenant_id=tenant_id,
                dependency_ref=self._dependencies.next_dependency_ref(tenant_id),
                job_ref=job.job_ref,
                depends_on_job_ref=parent.job_ref,
            )
            job.depends_on.append(parent.job_ref)
            await self._dependencies.save(dep)
            await self._jobs.save(job)
            dep_count += 1

        exec_count = 0
        for edata in seed_data["executions"]:
            job = created_jobs[edata["job_index"]]
            execution = JobExecution.start(
                tenant_id=tenant_id,
                execution_ref=self._executions.next_execution_ref(tenant_id),
                job_ref=job.job_ref,
                attempt=edata.get("attempt", 1),
                worker_shard=job.worker_shard,
            )
            if edata["status"] == ExecutionStatus.SUCCEEDED.value:
                execution.complete(duration_ms=edata.get("duration_ms", 0))
            else:
                execution.fail(error_message=edata.get("error", "failed"), duration_ms=edata.get("duration_ms", 0))
            await self._executions.save(execution)
            exec_count += 1

        return Result.ok({
            "seeded": True,
            "jobs": len(created_jobs),
            "dependencies": dep_count,
            "executions": exec_count,
        })

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        jobs = [j.to_dict() for j in await self._jobs.list_by_tenant(tenant_id)]
        executions = [e.to_dict() for e in await self._executions.list_by_tenant(tenant_id)]
        deps = [d.to_dict() for d in await self._dependencies.list_by_tenant(tenant_id)]
        dashboard = engine.build_dashboard(profile=profile.to_dict() if profile else None, jobs=jobs, executions=executions, dependencies=deps)
        monitoring = dashboard["summary"]
        await publish_integration_event(
            SchedulerDashboardGeneratedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                jobs_total=monitoring["jobs_total"],
                executions_total=monitoring["executions_total"],
                success_rate_pct=monitoring["success_rate_pct"],
            )
        )
        return Result.ok(dashboard)

    async def list_jobs(self, tenant_id: str) -> Result[list[dict]]:
        jobs = await self._jobs.list_by_tenant(tenant_id)
        return Result.ok([j.to_dict() for j in jobs])

    async def create_job(
        self,
        tenant_id: str,
        *,
        name: str,
        job_type: str,
        cron_expression: str = "",
        calendar_rule: str = "",
        recurrence_rule: str = "",
        event_pattern: str = "",
        workflow_ref: str = "",
        priority: int | None = None,
        max_retries: int | None = None,
        depends_on: list[str] | None = None,
        payload: dict | None = None,
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        type_gate = {
            "cron": policy["cron_enabled"],
            "calendar": policy["calendar_enabled"],
            "recurring": policy["recurring_enabled"],
            "event": policy["event_trigger_enabled"],
            "workflow": policy["workflow_trigger_enabled"],
        }
        if not type_gate.get(job_type, True):
            return Result.fail(f"job_type_disabled:{job_type}")

        job_ref = self._jobs.next_job_ref(tenant_id)
        shard = engine.resolve_worker_shard(job_ref=job_ref) if policy["distributed_enabled"] else "default"
        job = ScheduledJob.define(
            tenant_id=tenant_id,
            job_ref=job_ref,
            name=name,
            job_type=job_type,
            cron_expression=cron_expression,
            calendar_rule=calendar_rule,
            recurrence_rule=recurrence_rule,
            event_pattern=event_pattern,
            workflow_ref=workflow_ref,
            priority=priority if priority is not None and policy["priority_enabled"] else policy["default_priority"],
            max_retries=max_retries if max_retries is not None else policy["max_retries"],
            depends_on=depends_on,
            worker_shard=shard,
            payload=payload,
        )
        job.next_run_at = datetime.now(UTC) + timedelta(minutes=5)
        await self._jobs.save(job)
        await publish_integration_event(
            JobScheduledIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                job_ref=job.job_ref,
                job_type=job.job_type,
                next_run_at=job.next_run_at.isoformat(),
            )
        )
        return Result.ok(job.to_dict())

    async def get_job(self, tenant_id: str, job_ref: str) -> Result[dict]:
        job = await self._jobs.find_by_ref(tenant_id, job_ref)
        if not job:
            return Result.fail("job_not_found")
        return Result.ok(job.to_dict())

    async def trigger_job(self, tenant_id: str, job_ref: str, *, correlation_id: str = "") -> Result[dict]:
        job = await self._jobs.find_by_ref(tenant_id, job_ref)
        if not job:
            return Result.fail("job_not_found")
        if job.status == JobStatus.PAUSED.value:
            return Result.fail("job_paused")

        policy = await self._policy_params(tenant_id)
        deps = [d.to_dict() for d in await self._dependencies.list_by_tenant(tenant_id)]
        execs = [e.to_dict() for e in await self._executions.list_by_tenant(tenant_id)]
        if not engine.dependencies_satisfied(job=job.to_dict(), dependencies=deps, executions=execs):
            return Result.fail("dependencies_not_satisfied")

        execution = JobExecution.start(
            tenant_id=tenant_id,
            execution_ref=self._executions.next_execution_ref(tenant_id),
            job_ref=job.job_ref,
            attempt=job.retry_count + 1,
            worker_shard=job.worker_shard,
            correlation_id=correlation_id or str(uuid.uuid4()),
        )
        job.status = JobStatus.RUNNING.value
        job.last_run_at = datetime.now(UTC)
        await self._jobs.save(job)
        await self._executions.save(execution)
        await publish_integration_event(
            JobStartedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=execution.correlation_id,
                job_ref=job.job_ref,
                execution_ref=execution.execution_ref,
                worker_shard=job.worker_shard,
            )
        )

        duration_ms = 120.0
        execution.complete(duration_ms=duration_ms)
        job.status = JobStatus.SCHEDULED.value
        job.next_run_at = datetime.now(UTC) + timedelta(hours=1)
        await self._executions.save(execution)
        await self._jobs.save(job)
        await publish_integration_event(
            JobCompletedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=execution.correlation_id,
                job_ref=job.job_ref,
                execution_ref=execution.execution_ref,
                duration_ms=duration_ms,
            )
        )
        return Result.ok({"job": job.to_dict(), "execution": execution.to_dict()})

    async def pause_job(self, tenant_id: str, job_ref: str) -> Result[dict]:
        job = await self._jobs.find_by_ref(tenant_id, job_ref)
        if not job:
            return Result.fail("job_not_found")
        job.pause()
        await self._jobs.save(job)
        return Result.ok(job.to_dict())

    async def resume_job(self, tenant_id: str, job_ref: str) -> Result[dict]:
        job = await self._jobs.find_by_ref(tenant_id, job_ref)
        if not job:
            return Result.fail("job_not_found")
        job.resume()
        await self._jobs.save(job)
        return Result.ok(job.to_dict())

    async def list_history(self, tenant_id: str, job_ref: str | None = None) -> Result[list[dict]]:
        if job_ref:
            executions = await self._executions.list_by_job(tenant_id, job_ref)
        else:
            executions = await self._executions.list_by_tenant(tenant_id)
        return Result.ok([e.to_dict() for e in executions])

    async def list_dependencies(self, tenant_id: str) -> Result[list[dict]]:
        deps = await self._dependencies.list_by_tenant(tenant_id)
        return Result.ok([d.to_dict() for d in deps])

    async def register_dependency(
        self,
        tenant_id: str,
        *,
        job_ref: str,
        depends_on_job_ref: str,
        required_status: str = ExecutionStatus.SUCCEEDED.value,
    ) -> Result[dict]:
        job = await self._jobs.find_by_ref(tenant_id, job_ref)
        parent = await self._jobs.find_by_ref(tenant_id, depends_on_job_ref)
        if not job or not parent:
            return Result.fail("job_not_found")
        dep = JobDependency.link(
            tenant_id=tenant_id,
            dependency_ref=self._dependencies.next_dependency_ref(tenant_id),
            job_ref=job_ref,
            depends_on_job_ref=depends_on_job_ref,
            required_status=required_status,
        )
        if depends_on_job_ref not in job.depends_on:
            job.depends_on.append(depends_on_job_ref)
        await self._dependencies.save(dep)
        await self._jobs.save(job)
        return Result.ok(dep.to_dict())

    async def get_monitoring(self, tenant_id: str) -> Result[dict]:
        jobs = [j.to_dict() for j in await self._jobs.list_by_tenant(tenant_id)]
        executions = [e.to_dict() for e in await self._executions.list_by_tenant(tenant_id)]
        return Result.ok(engine.build_monitoring(jobs=jobs, executions=executions))
