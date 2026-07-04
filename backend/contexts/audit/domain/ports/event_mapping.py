"""Audit event mapping port — implemented in infrastructure/acl/."""
from __future__ import annotations

from typing import Protocol

from contexts.audit.domain.aggregates.audit_entry import AuditEntry


class IAuditEventMapper(Protocol):
    def map_envelope(self, envelope: dict) -> AuditEntry: ...
