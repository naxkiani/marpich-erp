"""Enterprise Regulatory Reporting Platform application service."""
from __future__ import annotations

from contexts.regulatory_reporting.domain.aggregates.regulatory_reporting_platform import (
    CountryAdapter,
    DigitalSubmission,
    RegulatorType,
    RegulatoryTenantProfile,
    SubmissionStatus,
)
from contexts.regulatory_reporting.domain.events.regulatory_reporting_integration_events import (
    CountryAdapterConfiguredIntegration,
    DigitalSubmissionCreatedIntegration,
    DigitalSubmissionSubmittedIntegration,
)
from contexts.regulatory_reporting.domain.ports.regulatory_reporting_repositories import (
    ICountryAdapterRepository,
    IDigitalSubmissionRepository,
    IRegulatoryTenantProfileRepository,
)
from contexts.regulatory_reporting.domain.services import regulatory_reporting_engine
from contexts.regulatory_reporting.infrastructure.acl.reporting_acl import ReportingRegulatoryAcl
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class EnterpriseRegulatoryReportingApplicationService:
    def __init__(
        self,
        profiles: IRegulatoryTenantProfileRepository,
        adapters: ICountryAdapterRepository,
        submissions: IDigitalSubmissionRepository,
        reporting_acl: ReportingRegulatoryAcl,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._adapters = adapters
        self._submissions = submissions
        self._reporting = reporting_acl
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        params = {
            "default_format": "json",
            "package_required": True,
            "submission_audit": True,
            "digital_submission_enabled": True,
            "default_country": "EXAMPLE",
        }
        pmap = {
            "regulatory_reporting.default_format": ("default_format", "format"),
            "regulatory_reporting.package.required": ("package_required", "required"),
            "regulatory_reporting.submission.audit": ("submission_audit", "audit"),
            "regulatory_reporting.digital_submission.enabled": ("digital_submission_enabled", "enabled"),
            "regulatory_reporting.country.default": ("default_country", "country_code"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(
                tenant_id=tenant_id, domain="tax", policy_key=key, facts={}
            )
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": regulatory_reporting_engine.list_capability_catalog(),
            "regulators": regulatory_reporting_engine.list_regulators(),
            "report_categories": regulatory_reporting_engine.list_report_categories(),
            "export_formats": regulatory_reporting_engine.list_export_formats(),
            "policy_keys": regulatory_reporting_engine.list_policy_keys(),
            "shared_service": True,
            "delegation": {
                "reporting_engine_rendering": True,
                "manifest_driven_formats": True,
                "hardcoded_regulatory_formats": False,
                "local_format_duplication": False,
            },
        })

    async def get_dependency_map(self) -> Result[dict]:
        return Result.ok(regulatory_reporting_engine.dependency_map())

    async def seed(self, tenant_id: str) -> Result[dict]:
        existing = await self._profiles.find_by_tenant(tenant_id)
        if existing and await self._adapters.list_by_tenant(tenant_id):
            return Result.ok({
                "seeded": False,
                "profile": existing.to_dict(),
                "adapters": len(await self._adapters.list_by_tenant(tenant_id)),
            })

        params = await self._policy_params(tenant_id)
        if not existing:
            ref = self._profiles.next_profile_ref(tenant_id)
            profile = RegulatoryTenantProfile.create(
                tenant_id=tenant_id,
                profile_ref=ref,
                enabled_regulators=[r.value for r in RegulatorType],
            )
            profile.default_format = str(params.get("default_format", "json"))
            profile.default_country = str(params.get("default_country", "EXAMPLE"))
            profile.digital_submission_enabled = bool(params.get("digital_submission_enabled", True))
            await self._profiles.save(profile)
        else:
            profile = existing

        await self._reporting.seed_reporting_packages(tenant_id)

        adapters_seeded = 0
        for seed_adapter in regulatory_reporting_engine.DEFAULT_COUNTRY_ADAPTERS:
            existing_adapter = await self._adapters.find_by_country(
                tenant_id, seed_adapter["country_code"]
            )
            if existing_adapter:
                continue
            adapter_ref = self._adapters.next_adapter_ref(tenant_id)
            adapter = CountryAdapter.configure(
                tenant_id=tenant_id,
                adapter_ref=adapter_ref,
                country_code=seed_adapter["country_code"],
                country_name=seed_adapter["country_name"],
                regulator_types=seed_adapter["regulator_types"],
                supported_formats=seed_adapter["supported_formats"],
                package_plugin_id=seed_adapter["package_plugin_id"],
                portal_url=seed_adapter["portal_url"],
            )
            await self._adapters.save(adapter)
            adapters_seeded += 1

        return Result.ok({
            "seeded": True,
            "profile": profile.to_dict(),
            "adapters_seeded": adapters_seeded,
            "reporting_packages_seeded": True,
            "enabled_regulators": len(profile.enabled_regulators),
        })

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        adapters = [a.to_dict() for a in await self._adapters.list_by_tenant(tenant_id)]
        submissions = [s.to_dict() for s in await self._submissions.list_by_tenant(tenant_id)]
        return Result.ok(
            regulatory_reporting_engine.build_dashboard(
                profile=profile.to_dict() if profile else None,
                adapters=adapters,
                submissions=submissions,
            )
        )

    async def list_adapters(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._adapters.list_by_tenant(tenant_id)
        return Result.ok([a.to_dict() for a in items])

    async def configure_adapter(
        self,
        tenant_id: str,
        *,
        country_code: str,
        country_name: str,
        regulator_types: list[str],
        supported_formats: list[str],
        package_plugin_id: str = "",
        portal_url: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        existing = await self._adapters.find_by_country(tenant_id, country_code)
        if existing:
            return Result.ok(existing.to_dict())

        adapter_ref = self._adapters.next_adapter_ref(tenant_id)
        adapter = CountryAdapter.configure(
            tenant_id=tenant_id,
            adapter_ref=adapter_ref,
            country_code=country_code,
            country_name=country_name,
            regulator_types=regulator_types,
            supported_formats=supported_formats,
            package_plugin_id=package_plugin_id,
            portal_url=portal_url,
        )
        await self._adapters.save(adapter)

        corr = correlation_id or adapter_ref
        await publish_integration_event(
            CountryAdapterConfiguredIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                adapter_ref=adapter_ref,
                country_code=country_code.upper(),
            )
        )
        return Result.ok(adapter.to_dict())

    async def generate_report(
        self,
        tenant_id: str,
        *,
        country_code: str,
        regulator_type: str = "",
        report_category: str = "",
        export_format: str = "",
        parameters: dict | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        adapter = await self._adapters.find_by_country(tenant_id, country_code)
        if not adapter:
            return Result.fail("country_adapter_not_found")

        fmt = (export_format or str(params.get("default_format", "json"))).lower()
        if fmt not in adapter.supported_formats:
            return Result.fail(f"format_not_supported:{fmt}")

        if regulator_type and regulator_type not in adapter.regulator_types:
            return Result.fail("regulator_not_supported_for_country")

        report_type = regulatory_reporting_engine.resolve_report_type(
            regulator_type=regulator_type, report_category=report_category
        )

        package_ref = await self._reporting.get_package_ref_for_plugin(
            tenant_id, adapter.package_plugin_id
        )
        if not package_ref and bool(params.get("package_required", True)):
            seed = await self._reporting.seed_reporting_packages(tenant_id)
            if seed.succeeded:
                package_ref = await self._reporting.get_package_ref_for_plugin(
                    tenant_id, adapter.package_plugin_id
                )
        if not package_ref:
            return Result.fail("reporting_package_not_installed")

        render_result = await self._reporting.submit_report(
            tenant_id,
            package_ref=package_ref,
            report_type=report_type,
            export_format=fmt,
            parameters=parameters,
            correlation_id=correlation_id,
        )
        if not render_result.succeeded:
            return render_result

        reporting_sub = render_result.unwrap()
        submission_ref = self._submissions.next_submission_ref(tenant_id)
        submission = DigitalSubmission.create(
            tenant_id=tenant_id,
            submission_ref=submission_ref,
            adapter_ref=adapter.adapter_ref,
            country_code=adapter.country_code,
            regulator_type=regulator_type or report_category or "compliance",
            report_category=report_category or regulator_type or "compliance",
            export_format=fmt,
            reporting_submission_ref=reporting_sub.get("submission_ref", ""),
            metadata={"output": reporting_sub.get("output", {})},
        )
        submission.mark_rendered(reporting_sub.get("submission_ref", ""))
        await self._submissions.save(submission)

        corr = correlation_id or submission_ref
        await publish_integration_event(
            DigitalSubmissionCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                submission_ref=submission_ref,
                country_code=adapter.country_code,
                regulator_type=submission.regulator_type,
                export_format=fmt,
            )
        )
        return Result.ok({
            "submission": submission.to_dict(),
            "reporting_output": reporting_sub,
            "manifest_driven": True,
            "hardcoded_regulatory_formats": False,
        })

    async def submit_digitally(
        self,
        tenant_id: str,
        submission_ref: str,
        *,
        correlation_id: str = "",
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not bool(params.get("digital_submission_enabled", True)):
            return Result.fail("digital_submission_disabled")

        submission = await self._submissions.find_by_ref(tenant_id, submission_ref)
        if not submission:
            return Result.fail("submission_not_found")
        if submission.status not in (SubmissionStatus.RENDERED.value, SubmissionStatus.DRAFT.value):
            return Result.fail("submission_not_ready")

        adapter = await self._adapters.find_by_ref(tenant_id, submission.adapter_ref)
        portal_ref = f"PORTAL-{submission.country_code}-{submission_ref[-8:]}"
        submission.submit(portal_reference=portal_ref)
        await self._submissions.save(submission)

        corr = correlation_id or submission_ref
        await publish_integration_event(
            DigitalSubmissionSubmittedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                submission_ref=submission_ref,
                portal_reference=portal_ref,
            )
        )
        return Result.ok({
            "submission": submission.to_dict(),
            "portal_url": adapter.portal_url if adapter else "",
            "portal_reference": portal_ref,
        })

    async def list_submissions(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._submissions.list_by_tenant(tenant_id)
        return Result.ok([s.to_dict() for s in items])

    async def get_submission(self, tenant_id: str, submission_ref: str) -> Result[dict]:
        item = await self._submissions.find_by_ref(tenant_id, submission_ref)
        if not item:
            return Result.fail("submission_not_found")
        return Result.ok(item.to_dict())

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope.get("tenant_id", "")
        if tenant_id:
            await self.seed(tenant_id)
