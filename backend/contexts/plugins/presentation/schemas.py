"""Plugin API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class RegisterPluginRequest(BaseModel):
    plugin_id: str
    plugin_type: str
    display_name: str
    description: str = ""
    publisher_id: str
    publisher_name: str
    version: str
    permissions: list[str] = Field(default_factory=list)
    extension_points: list[str]
    sandbox_profile: str | None = None
    trust_level: str = "community"
    signature_algorithm: str = "ed25519"
    public_key_fingerprint: str
    package_checksum: str


class InstallPluginRequest(BaseModel):
    granted_permissions: list[str]
    config: dict | None = None


class UpgradePluginRequest(BaseModel):
    target_version: str


class SubmitListingRequest(BaseModel):
    version: str
    package_checksum: str
    public_key_fingerprint: str


class InvokePluginRequest(BaseModel):
    plugin_id: str
    extension_point: str
    payload: dict = Field(default_factory=dict)
