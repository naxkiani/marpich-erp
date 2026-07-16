"""Enterprise Regulatory Reporting Platform API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ConfigureAdapterRequest(BaseModel):
    country_code: str
    country_name: str
    regulator_types: list[str] = Field(default_factory=list)
    supported_formats: list[str] = Field(default_factory=lambda: ["xml", "json", "pdf"])
    package_plugin_id: str = ""
    portal_url: str = ""


class GenerateReportRequest(BaseModel):
    country_code: str
    regulator_type: str = ""
    report_category: str = ""
    export_format: str = ""
    parameters: dict = Field(default_factory=dict)
