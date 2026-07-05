"""Enterprise account hierarchy — multiple trees, versioning, templates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class TreeType(StrEnum):
    PRIMARY = "primary"
    AUXILIARY = "auxiliary"
    STATUTORY = "statutory"
    MANAGEMENT = "management"
    CONSOLIDATION = "consolidation"


class TreeChangeType(StrEnum):
    CREATE = "create"
    MOVE = "move"
    IMPORT = "import"
    EXPORT = "export"
    TEMPLATE_APPLY = "template_apply"
    MANUAL_SNAPSHOT = "manual_snapshot"
    RESTORE = "restore"


@dataclass(eq=False, kw_only=True)
class AccountTree(AggregateRoot):
    tenant_id: str
    name: str
    description: str = ""
    tree_type: str = TreeType.PRIMARY.value
    template_key: str | None = None
    template_type: str | None = None
    country_code: str | None = None
    is_default: bool = False
    is_active: bool = True
    current_version: int = 1
    account_count: int = 0
    max_depth: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        name: str,
        description: str = "",
        tree_type: str = TreeType.PRIMARY.value,
        template_key: str | None = None,
        template_type: str | None = None,
        country_code: str | None = None,
        is_default: bool = False,
    ) -> AccountTree:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            name=name.strip(),
            description=description,
            tree_type=tree_type,
            template_key=template_key,
            template_type=template_type,
            country_code=country_code,
            is_default=is_default,
        )

    def bump_version(self) -> int:
        self.current_version += 1
        return self.current_version

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "name": self.name,
            "description": self.description,
            "tree_type": self.tree_type,
            "template_key": self.template_key,
            "template_type": self.template_type,
            "country_code": self.country_code,
            "is_default": self.is_default,
            "is_active": self.is_active,
            "current_version": self.current_version,
            "account_count": self.account_count,
            "max_depth": self.max_depth,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class AccountTreeVersion(AggregateRoot):
    tenant_id: str
    tree_id: str
    version_number: int
    snapshot: list[dict]
    change_type: str
    change_summary: str = ""
    actor_id: str = "system"
    account_count: int = 0
    max_depth: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        tree_id: str,
        version_number: int,
        snapshot: list[dict],
        change_type: str,
        change_summary: str = "",
        actor_id: str = "system",
        account_count: int = 0,
        max_depth: int = 0,
    ) -> AccountTreeVersion:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            tree_id=tree_id,
            version_number=version_number,
            snapshot=snapshot,
            change_type=change_type,
            change_summary=change_summary,
            actor_id=actor_id,
            account_count=account_count,
            max_depth=max_depth,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "tree_id": self.tree_id,
            "version_number": self.version_number,
            "snapshot": self.snapshot,
            "change_type": self.change_type,
            "change_summary": self.change_summary,
            "actor_id": self.actor_id,
            "account_count": self.account_count,
            "max_depth": self.max_depth,
            "created_at": self.created_at.isoformat(),
        }
