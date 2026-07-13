"""Enterprise Integration Studio application service."""
from __future__ import annotations

import uuid

from contexts.enterprise_integration_studio.domain.aggregates.enterprise_integration_studio_platform import (
    ArtifactStatus,
    ArtifactType,
    MarketplaceListing,
    StudioArtifact,
    StudioDeployment,
    StudioProfile,
    StudioProject,
    StudioTestRun,
    StudioVersion,
)
from contexts.enterprise_integration_studio.domain.events.enterprise_integration_studio_integration_events import (
    ArtifactCreatedIntegration,
    DeploymentCompletedIntegration,
    StudioDashboardGeneratedIntegration,
    TestCompletedIntegration,
    VersionPublishedIntegration,
)
from contexts.enterprise_integration_studio.domain.ports.enterprise_integration_studio_repositories import (
    IMarketplaceListingRepository,
    IStudioArtifactRepository,
    IStudioDeploymentRepository,
    IStudioProfileRepository,
    IStudioProjectRepository,
    IStudioTestRunRepository,
    IStudioVersionRepository,
)
from contexts.enterprise_integration_studio.domain.services import enterprise_integration_studio_engine as engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class EnterpriseIntegrationStudioApplicationService:
    def __init__(
        self,
        profiles: IStudioProfileRepository,
        projects: IStudioProjectRepository,
        artifacts: IStudioArtifactRepository,
        versions: IStudioVersionRepository,
        deployments: IStudioDeploymentRepository,
        tests: IStudioTestRunRepository,
        marketplace: IMarketplaceListingRepository,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._projects = projects
        self._artifacts = artifacts
        self._versions = versions
        self._deployments = deployments
        self._tests = tests
        self._marketplace = marketplace
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "api_builder_enabled": profile.api_builder_enabled if profile else True,
            "connector_builder_enabled": profile.connector_builder_enabled if profile else True,
            "workflow_builder_enabled": profile.workflow_builder_enabled if profile else True,
            "event_designer_enabled": profile.event_designer_enabled if profile else True,
            "testing_enabled": profile.testing_enabled if profile else True,
            "mock_services_enabled": profile.mock_services_enabled if profile else True,
            "marketplace_enabled": profile.marketplace_enabled if profile else True,
            "citizen_workspace_enabled": profile.citizen_workspace_enabled if profile else True,
        }
        pmap = {
            "enterprise_integration_studio.api_builder.enabled": ("api_builder_enabled", "enabled"),
            "enterprise_integration_studio.connector_builder.enabled": ("connector_builder_enabled", "enabled"),
            "enterprise_integration_studio.workflow_builder.enabled": ("workflow_builder_enabled", "enabled"),
            "enterprise_integration_studio.event_designer.enabled": ("event_designer_enabled", "enabled"),
            "enterprise_integration_studio.testing.enabled": ("testing_enabled", "enabled"),
            "enterprise_integration_studio.mock_services.enabled": ("mock_services_enabled", "enabled"),
            "enterprise_integration_studio.marketplace.enabled": ("marketplace_enabled", "enabled"),
            "enterprise_integration_studio.citizen_workspace.enabled": ("citizen_workspace_enabled", "enabled"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> StudioProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = StudioProfile.create(
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
            "artifact_types": [t.value for t in ArtifactType],
            "delegation": {
                "api_runtime": "enterprise_api_gateway",
                "connectors": "enterprise_connector_framework",
                "workflows": "workflow",
                "events": "enterprise_event_bus",
                "local_integration_duplication": False,
            },
        })

    async def get_dependency_map(self) -> Result[dict]:
        return Result.ok(engine.dependency_map())

    async def seed(self, tenant_id: str) -> Result[dict]:
        await self._ensure_profile(tenant_id)
        seed_data = engine.generate_seed_data()
        created_projects: list[StudioProject] = []
        for pdata in seed_data["projects"]:
            project = StudioProject.create(
                tenant_id=tenant_id,
                project_ref=self._projects.next_project_ref(tenant_id),
                name=pdata["name"],
                workspace_type=pdata["workspace_type"],
                description=pdata.get("description", ""),
            )
            await self._projects.save(project)
            created_projects.append(project)

        artifact_count = 0
        for adata in seed_data["artifacts"]:
            project = created_projects[adata["project_index"]]
            graph = engine.build_designer_graph(artifact_type=adata["artifact_type"], artifact=adata)
            artifact = StudioArtifact.create(
                tenant_id=tenant_id,
                artifact_ref=self._artifacts.next_artifact_ref(tenant_id),
                project_ref=project.project_ref,
                name=adata["name"],
                artifact_type=adata["artifact_type"],
                designer_graph=graph,
                mapping=seed_data.get("mapping", {}) if adata["artifact_type"] == "connector" else {},
                transformation=seed_data.get("transformation", {}) if adata["artifact_type"] in ("connector", "api") else {},
                openapi=engine.build_openapi_documentation(artifact={"name": adata["name"], "artifact_ref": "seed"}),
            )
            await self._artifacts.save(artifact)
            project.artifact_count += 1
            await self._projects.save(project)
            artifact_count += 1
            await publish_integration_event(
                ArtifactCreatedIntegration(
                    tenant_id=TenantId(tenant_id),
                    correlation_id=str(uuid.uuid4()),
                    artifact_ref=artifact.artifact_ref,
                    artifact_type=artifact.artifact_type,
                    project_ref=project.project_ref,
                )
            )

        mkt_count = 0
        for mdata in seed_data["marketplace"]:
            listing = MarketplaceListing.list_connector(
                tenant_id=tenant_id,
                listing_ref=self._marketplace.next_listing_ref(tenant_id),
                connector_type=mdata["connector_type"],
                name=mdata["name"],
                publisher=mdata["publisher"],
                version=mdata["version"],
            )
            await self._marketplace.save(listing)
            mkt_count += 1

        return Result.ok({
            "seeded": True,
            "projects": len(created_projects),
            "artifacts": artifact_count,
            "marketplace_listings": mkt_count,
        })

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        projects = [p.to_dict() for p in await self._projects.list_by_tenant(tenant_id)]
        artifacts = [a.to_dict() for a in await self._artifacts.list_by_tenant(tenant_id)]
        versions = [v.to_dict() for v in await self._versions.list_by_tenant(tenant_id)]
        deployments = [d.to_dict() for d in await self._deployments.list_by_tenant(tenant_id)]
        tests = [t.to_dict() for t in await self._tests.list_by_tenant(tenant_id)]
        marketplace = [m.to_dict() for m in await self._marketplace.list_by_tenant(tenant_id)]
        dashboard = engine.build_dashboard(
            profile=profile.to_dict() if profile else None,
            projects=projects,
            artifacts=artifacts,
            versions=versions,
            deployments=deployments,
            tests=tests,
            marketplace=marketplace,
        )
        await publish_integration_event(
            StudioDashboardGeneratedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                projects_total=dashboard["summary"]["projects"],
                artifacts_total=dashboard["summary"]["artifacts"],
                deployments_live=dashboard["summary"]["deployments_live"],
            )
        )
        return Result.ok(dashboard)

    async def get_developer_portal(self, tenant_id: str) -> Result[dict]:
        projects = [p.to_dict() for p in await self._projects.list_by_tenant(tenant_id)]
        artifacts = [a.to_dict() for a in await self._artifacts.list_by_tenant(tenant_id)]
        marketplace = [m.to_dict() for m in await self._marketplace.list_by_tenant(tenant_id)]
        return Result.ok(engine.build_developer_portal(projects=projects, artifacts=artifacts, marketplace=marketplace))

    async def get_citizen_workspace(self, tenant_id: str) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["citizen_workspace_enabled"]:
            return Result.fail("citizen_workspace_disabled")
        projects = [p.to_dict() for p in await self._projects.list_by_tenant(tenant_id)]
        artifacts = [a.to_dict() for a in await self._artifacts.list_by_tenant(tenant_id)]
        return Result.ok(engine.build_citizen_workspace(projects=projects, artifacts=artifacts))

    async def list_marketplace(self, tenant_id: str) -> Result[list[dict]]:
        listings = await self._marketplace.list_by_tenant(tenant_id)
        return Result.ok([l.to_dict() for l in listings])

    async def list_projects(self, tenant_id: str) -> Result[list[dict]]:
        return Result.ok([p.to_dict() for p in await self._projects.list_by_tenant(tenant_id)])

    async def create_project(
        self,
        tenant_id: str,
        *,
        name: str,
        workspace_type: str = "developer",
        description: str = "",
    ) -> Result[dict]:
        if workspace_type == "citizen":
            policy = await self._policy_params(tenant_id)
            if not policy["citizen_workspace_enabled"]:
                return Result.fail("citizen_workspace_disabled")
        project = StudioProject.create(
            tenant_id=tenant_id,
            project_ref=self._projects.next_project_ref(tenant_id),
            name=name,
            workspace_type=workspace_type,
            description=description,
        )
        await self._projects.save(project)
        return Result.ok(project.to_dict())

    async def list_artifacts(self, tenant_id: str) -> Result[list[dict]]:
        return Result.ok([a.to_dict() for a in await self._artifacts.list_by_tenant(tenant_id)])

    async def create_artifact(
        self,
        tenant_id: str,
        *,
        project_ref: str,
        name: str,
        artifact_type: str,
        mapping: dict | None = None,
        transformation: dict | None = None,
    ) -> Result[dict]:
        project = await self._projects.find_by_ref(tenant_id, project_ref)
        if not project:
            return Result.fail("project_not_found")
        policy = await self._policy_params(tenant_id)
        gates = {
            "api": policy["api_builder_enabled"],
            "connector": policy["connector_builder_enabled"],
            "workflow": policy["workflow_builder_enabled"],
            "event": policy["event_designer_enabled"],
            "mock": policy["mock_services_enabled"],
            "mapping": True,
        }
        if not gates.get(artifact_type, True):
            return Result.fail(f"artifact_type_disabled:{artifact_type}")

        artifact_ref = self._artifacts.next_artifact_ref(tenant_id)
        adata = {"name": name, "artifact_ref": artifact_ref}
        artifact = StudioArtifact.create(
            tenant_id=tenant_id,
            artifact_ref=artifact_ref,
            project_ref=project_ref,
            name=name,
            artifact_type=artifact_type,
            designer_graph=engine.build_designer_graph(artifact_type=artifact_type, artifact=adata),
            mapping=mapping or {},
            transformation=transformation or {},
            openapi=engine.build_openapi_documentation(artifact=adata) if artifact_type == "api" else {},
        )
        await self._artifacts.save(artifact)
        project.artifact_count += 1
        await self._projects.save(project)
        await publish_integration_event(
            ArtifactCreatedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                artifact_ref=artifact.artifact_ref,
                artifact_type=artifact.artifact_type,
                project_ref=project_ref,
            )
        )
        return Result.ok(artifact.to_dict())

    async def get_designer(self, tenant_id: str, artifact_ref: str) -> Result[dict]:
        artifact = await self._artifacts.find_by_ref(tenant_id, artifact_ref)
        if not artifact:
            return Result.fail("artifact_not_found")
        return Result.ok(artifact.designer_graph)

    async def get_documentation(self, tenant_id: str, artifact_ref: str) -> Result[dict]:
        artifact = await self._artifacts.find_by_ref(tenant_id, artifact_ref)
        if not artifact:
            return Result.fail("artifact_not_found")
        doc = artifact.openapi or engine.build_openapi_documentation(artifact=artifact.to_dict())
        return Result.ok(doc)

    async def test_artifact(self, tenant_id: str, artifact_ref: str, *, use_mock: bool = True) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["testing_enabled"]:
            return Result.fail("testing_disabled")
        if use_mock and not policy["mock_services_enabled"]:
            return Result.fail("mock_services_disabled")
        artifact = await self._artifacts.find_by_ref(tenant_id, artifact_ref)
        if not artifact:
            return Result.fail("artifact_not_found")
        result = engine.run_mock_test(artifact=artifact.to_dict(), use_mock=use_mock)
        test_run = StudioTestRun.run(
            tenant_id=tenant_id,
            test_ref=self._tests.next_test_ref(tenant_id),
            artifact_ref=artifact_ref,
            status=result["status"],
            assertions_passed=result["assertions_passed"],
            assertions_failed=result["assertions_failed"],
            duration_ms=result["duration_ms"],
            mock_used=result["mock_used"],
            report=result["report"],
        )
        if result["status"] == "passed":
            artifact.status = ArtifactStatus.TESTED.value
            await self._artifacts.save(artifact)
        await self._tests.save(test_run)
        await publish_integration_event(
            TestCompletedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                artifact_ref=artifact_ref,
                test_ref=test_run.test_ref,
                status=test_run.status,
            )
        )
        return Result.ok({"test": test_run.to_dict(), "result": result})

    async def publish_version(self, tenant_id: str, artifact_ref: str, *, changelog: str = "") -> Result[dict]:
        artifact = await self._artifacts.find_by_ref(tenant_id, artifact_ref)
        if not artifact:
            return Result.fail("artifact_not_found")
        parts = artifact.version.split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        new_version = ".".join(parts)
        artifact.version = new_version
        artifact.status = ArtifactStatus.PUBLISHED.value
        version = StudioVersion.publish(
            tenant_id=tenant_id,
            version_ref=self._versions.next_version_ref(tenant_id),
            artifact_ref=artifact_ref,
            version=new_version,
            changelog=changelog,
        )
        await self._artifacts.save(artifact)
        await self._versions.save(version)
        await publish_integration_event(
            VersionPublishedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                artifact_ref=artifact_ref,
                version=new_version,
            )
        )
        return Result.ok(version.to_dict())

    async def deploy_artifact(
        self,
        tenant_id: str,
        artifact_ref: str,
        *,
        environment: str = "sandbox",
    ) -> Result[dict]:
        artifact = await self._artifacts.find_by_ref(tenant_id, artifact_ref)
        if not artifact:
            return Result.fail("artifact_not_found")
        deployment = StudioDeployment.create(
            tenant_id=tenant_id,
            deployment_ref=self._deployments.next_deployment_ref(tenant_id),
            artifact_ref=artifact_ref,
            version=artifact.version,
            environment=environment,
        )
        deployment.mark_live()
        artifact.status = ArtifactStatus.DEPLOYED.value
        await self._deployments.save(deployment)
        await self._artifacts.save(artifact)
        await publish_integration_event(
            DeploymentCompletedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                deployment_ref=deployment.deployment_ref,
                artifact_ref=artifact_ref,
                environment=environment,
            )
        )
        return Result.ok(deployment.to_dict())

    async def list_versions(self, tenant_id: str) -> Result[list[dict]]:
        return Result.ok([v.to_dict() for v in await self._versions.list_by_tenant(tenant_id)])

    async def list_deployments(self, tenant_id: str) -> Result[list[dict]]:
        return Result.ok([d.to_dict() for d in await self._deployments.list_by_tenant(tenant_id)])

    async def list_test_runs(self, tenant_id: str) -> Result[list[dict]]:
        return Result.ok([t.to_dict() for t in await self._tests.list_by_tenant(tenant_id)])

    async def list_mocks(self, tenant_id: str) -> Result[list[dict]]:
        mocks = [a.to_dict() for a in await self._artifacts.list_by_tenant(tenant_id) if a.artifact_type == "mock"]
        return Result.ok(mocks)
