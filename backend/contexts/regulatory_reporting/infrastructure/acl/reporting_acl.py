"""ACL to reporting regulatory engine — no format duplication."""
from __future__ import annotations

from contexts.reporting.container import get_regulatory_reporting_service
from shared.application.result import Result


class ReportingRegulatoryAcl:
    async def seed_reporting_packages(self, tenant_id: str) -> Result[dict]:
        return await get_regulatory_reporting_service().seed_defaults(tenant_id)

    async def submit_report(
        self,
        tenant_id: str,
        *,
        package_ref: str,
        report_type: str,
        export_format: str,
        parameters: dict | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        return await get_regulatory_reporting_service().submit_report(
            tenant_id,
            package_ref=package_ref,
            report_type=report_type,
            export_format=export_format,
            parameters=parameters,
            correlation_id=correlation_id,
        )

    async def list_packages(self, tenant_id: str) -> Result[list[dict]]:
        return await get_regulatory_reporting_service().list_packages(tenant_id)

    async def get_package_ref_for_plugin(self, tenant_id: str, plugin_id: str) -> str | None:
        result = await self.list_packages(tenant_id)
        if not result.succeeded:
            return None
        for pkg in result.unwrap():
            if pkg.get("plugin_id") == plugin_id and pkg.get("is_installed"):
                return pkg.get("package_ref")
        return None
