from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BootstrapOrganizationCommand:
    tenant_id: str
    correlation_id: str
    name: str


@dataclass(frozen=True, slots=True)
class AssignMemberFromUserCreatedCommand:
    tenant_id: str
    correlation_id: str
    user_id: str
    display_name: str
