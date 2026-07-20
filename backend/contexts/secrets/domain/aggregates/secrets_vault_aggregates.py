"""P209-G Enterprise Secrets Management & Vault aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsVaultPlaintextForbiddenRoot(AggregateRoot):
    """Secrets must not be stored in plaintext."""

    tenant_id: str
    secret_ref: str
    encrypted: bool
    plaintext: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def store(
        cls,
        *,
        tenant_id: str,
        secret_ref: str,
        encrypted: bool = True,
        plaintext: bool = False,
    ) -> SecretsVaultPlaintextForbiddenRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.vault.tenant_required")
        if plaintext or not encrypted:
            raise ValueError("secrets.vault.secrets_stored_in_plaintext")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            secret_ref=secret_ref.strip(),
            encrypted=True,
            plaintext=False,
            status="stored",
        )
        root.pending_events.append("SecretCreated")
        root.pending_events.append("PlaintextSecretRejected")
        root.history.append({"event": "SecretStoredEncrypted"})
        return root

    def is_plaintext(self) -> bool:
        return self.plaintext or not self.encrypted


@dataclass(eq=False, kw_only=True)
class SecretsVaultNoHardcodingRoot(AggregateRoot):
    """Hardcoded credentials must not exist."""

    tenant_id: str
    scan_ref: str
    hardcoded: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def scan(
        cls,
        *,
        tenant_id: str,
        scan_ref: str,
        hardcoded: bool = False,
    ) -> SecretsVaultNoHardcodingRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.vault.hard_tenant_required")
        if hardcoded:
            raise ValueError("secrets.vault.hardcoded_credentials_exist")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            scan_ref=scan_ref.strip(),
            hardcoded=False,
            status="clean",
        )
        root.pending_events.append("HardcodedSecretBlocked")
        root.history.append({"event": "HardcodingScanClean"})
        return root

    def has_hardcoding(self) -> bool:
        return self.hardcoded


@dataclass(eq=False, kw_only=True)
class SecretsVaultSecretLifecycleRoot(AggregateRoot):
    """Secret lifecycle must be complete."""

    tenant_id: str
    secret_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def manage(
        cls,
        *,
        tenant_id: str,
        secret_ref: str,
        complete: bool = True,
    ) -> SecretsVaultSecretLifecycleRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.vault.life_tenant_required")
        if not complete:
            raise ValueError("secrets.vault.secret_lifecycle_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            secret_ref=secret_ref.strip(),
            complete=True,
            status="managed",
        )
        root.pending_events.append("SecretRegistered")
        root.history.append({"event": "SecretLifecycleManaged"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class SecretsVaultAutoRotationRoot(AggregateRoot):
    """Rotation must not be manual only."""

    tenant_id: str
    secret_ref: str
    automatic: bool
    manual_only: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        secret_ref: str,
        automatic: bool = True,
        manual_only: bool = False,
    ) -> SecretsVaultAutoRotationRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.vault.rot_tenant_required")
        if manual_only or not automatic:
            raise ValueError("secrets.vault.rotation_manual_only")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            secret_ref=secret_ref.strip(),
            automatic=True,
            manual_only=False,
            status="enabled",
        )
        root.pending_events.append("SecretRotated")
        root.history.append({"event": "AutoRotationEnabled"})
        return root

    def is_manual_only(self) -> bool:
        return self.manual_only or not self.automatic


@dataclass(eq=False, kw_only=True)
class SecretsVaultSecretOwnershipRoot(AggregateRoot):
    """Secret ownership must be known."""

    tenant_id: str
    secret_ref: str
    owner_ref: str
    known: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls,
        *,
        tenant_id: str,
        secret_ref: str,
        owner_ref: str,
        known: bool = True,
    ) -> SecretsVaultSecretOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.vault.own_tenant_required")
        if not known or not owner_ref.strip():
            raise ValueError("secrets.vault.secret_ownership_unknown")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            secret_ref=secret_ref.strip(),
            owner_ref=owner_ref.strip(),
            known=True,
            status="bound",
        )
        root.pending_events.append("SecretOwnershipBound")
        root.history.append({"event": "SecretOwnershipBound"})
        return root

    def is_unknown(self) -> bool:
        return not self.known or not self.owner_ref


@dataclass(eq=False, kw_only=True)
class SecretsVaultAccessAuditRoot(AggregateRoot):
    """Secret access must be audited."""

    tenant_id: str
    audit_ref: str
    action_ref: str
    audited: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        audit_ref: str,
        action_ref: str,
        audited: bool = True,
    ) -> SecretsVaultAccessAuditRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.vault.audit_tenant_required")
        if not audited:
            raise ValueError("secrets.vault.secret_access_unaudited")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            audit_ref=audit_ref.strip(),
            action_ref=action_ref.strip(),
            audited=True,
            status="recorded",
        )
        root.pending_events.append("SecretAuditRecorded")
        root.pending_events.append("SecretAccessGranted")
        root.history.append({"event": "SecretAccessAudited"})
        return root

    def is_unaudited(self) -> bool:
        return not self.audited


@dataclass(eq=False, kw_only=True)
class SecretsVaultDynamicCredentialsRoot(AggregateRoot):
    """Dynamic credentials must be supported."""

    tenant_id: str
    engine_ref: str
    supported: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        engine_ref: str,
        supported: bool = True,
    ) -> SecretsVaultDynamicCredentialsRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.vault.dyn_tenant_required")
        if not supported:
            raise ValueError("secrets.vault.dynamic_credentials_unsupported")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            engine_ref=engine_ref.strip(),
            supported=True,
            status="enabled",
        )
        root.pending_events.append("DynamicCredentialIssued")
        root.history.append({"event": "DynamicCredentialsEnabled"})
        return root

    def is_unsupported(self) -> bool:
        return not self.supported


@dataclass(eq=False, kw_only=True)
class SecretsVaultSecretLeaseRoot(AggregateRoot):
    """Secret lease with renew / revoke."""

    tenant_id: str
    lease_ref: str
    secret_ref: str
    active: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def issue(
        cls,
        *,
        tenant_id: str,
        lease_ref: str,
        secret_ref: str,
        active: bool = True,
    ) -> SecretsVaultSecretLeaseRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.vault.lease_tenant_required")
        if not active:
            raise ValueError("secrets.vault.dynamic_credentials_unsupported")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            lease_ref=lease_ref.strip(),
            secret_ref=secret_ref.strip(),
            active=True,
            status="active",
        )
        root.pending_events.append("SecretLeaseRenewed")
        root.pending_events.append("DynamicCredentialIssued")
        root.history.append({"event": "SecretLeaseIssued"})
        return root
