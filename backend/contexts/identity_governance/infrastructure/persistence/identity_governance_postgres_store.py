"""PostgreSQL repositories — Identity Governance SoR (matches Iga* ORM)."""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select

from contexts.identity_governance.domain.aggregates.identity_governance_platform import (
    AccessRequest,
    AccessReview,
    EmergencyAccessGrant,
    GovernanceAuditEntry,
    IdentityGovernanceProfile,
    PrivilegeCertification,
    TemporaryAccessGrant,
)
from contexts.identity_governance.domain.ports.identity_governance_repositories import (
    IAccessRequestRepository,
    IAccessReviewRepository,
    IEmergencyAccessGrantRepository,
    IGovernanceAuditEntryRepository,
    IIdentityGovernanceProfileRepository,
    IPrivilegeCertificationRepository,
    ITemporaryAccessGrantRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    IgaAccessRequestRow,
    IgaAccessReviewRow,
    IgaAuditEntryRow,
    IgaEmergencyAccessGrantRow,
    IgaPrivilegeCertificationRow,
    IgaProfileRow,
    IgaTemporaryAccessGrantRow,
)


def _uuid(value: UniqueId | str | UUID) -> UUID:
    if isinstance(value, UUID):
        return value
    return UUID(str(value))


def _parse_dt(value: datetime | str | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).replace("Z", "+00:00")
    return datetime.fromisoformat(text)


class _RefCounterMixin:
    _local_counters: dict[str, int] = {}

    def _local_next(self, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        n = self._local_counters.get(key, 0) + 1
        self._local_counters[key] = n
        return f"{prefix}-{tenant_id[:4].upper()}-{n:05d}"

    @classmethod
    def reset_counters(cls) -> None:
        cls._local_counters = {}


def _profile_from_row(row: object) -> IdentityGovernanceProfile:
    return IdentityGovernanceProfile(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        profile_ref=row.profile_ref,
        access_review_frequency_days=int(row.access_review_frequency_days),
        certification_required=bool(row.certification_required),
        sod_enforcement=bool(row.sod_enforcement),
        temporary_access_max_hours=int(row.temporary_access_max_hours),
        emergency_access_max_hours=int(row.emergency_access_max_hours),
        metadata=dict(row.metadata_json or {}),
        created_at=row.created_at or datetime.now(UTC),
    )


def _request_from_row(row: object) -> AccessRequest:
    return AccessRequest(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        request_ref=row.request_ref,
        requester_id=row.requester_id,
        target_user_id=row.target_user_id,
        requested_roles=list(row.requested_roles or []),
        justification=row.justification or "",
        status=row.status,
        approver_id=row.approver_id or "",
        sod_checked=bool(row.sod_checked),
        sod_valid=bool(row.sod_valid),
        metadata=dict(row.metadata_json or {}),
        created_at=row.created_at or datetime.now(UTC),
        updated_at=row.updated_at or datetime.now(UTC),
    )


def _review_from_row(row: object) -> AccessReview:
    completed = row.completed_at.isoformat() if row.completed_at else None
    return AccessReview(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        review_ref=row.review_ref,
        title=row.title,
        reviewer_id=row.reviewer_id,
        scope_user_ids=list(row.scope_user_ids or []),
        status=row.status,
        findings=list(row.findings or []),
        completed_at=completed,
        metadata=dict(row.metadata_json or {}),
        created_at=row.created_at or datetime.now(UTC),
    )


def _cert_from_row(row: object) -> PrivilegeCertification:
    certified = row.certified_at.isoformat() if row.certified_at else None
    return PrivilegeCertification(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        certification_ref=row.certification_ref,
        user_id=row.user_id,
        role_ids=list(row.role_ids or []),
        certifier_id=row.certifier_id or "",
        status=row.status,
        notes=row.notes or "",
        certified_at=certified,
        metadata=dict(row.metadata_json or {}),
        created_at=row.created_at or datetime.now(UTC),
    )


def _tmp_from_row(row: object) -> TemporaryAccessGrant:
    expires = row.expires_at.isoformat() if row.expires_at else ""
    return TemporaryAccessGrant(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        grant_ref=row.grant_ref,
        user_id=row.user_id,
        roles=list(row.roles or []),
        granted_by=row.granted_by,
        expires_at=expires,
        status=row.status,
        justification=row.justification or "",
        metadata=dict(row.metadata_json or {}),
        created_at=row.created_at or datetime.now(UTC),
    )


def _emg_from_row(row: object) -> EmergencyAccessGrant:
    expires = row.expires_at.isoformat() if row.expires_at else ""
    return EmergencyAccessGrant(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        grant_ref=row.grant_ref,
        user_id=row.user_id,
        roles=list(row.roles or []),
        granted_by=row.granted_by,
        expires_at=expires,
        status=row.status,
        incident_ref=row.incident_ref or "",
        justification=row.justification or "",
        metadata=dict(row.metadata_json or {}),
        created_at=row.created_at or datetime.now(UTC),
    )


def _audit_from_row(row: object) -> GovernanceAuditEntry:
    return GovernanceAuditEntry(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        entry_ref=row.entry_ref,
        action=row.action,
        actor_id=row.actor_id,
        resource_type=row.resource_type,
        resource_ref=row.resource_ref,
        details=dict(row.details or {}),
        created_at=row.created_at or datetime.now(UTC),
    )


class PostgresIdentityGovernanceProfileRepository(IIdentityGovernanceProfileRepository, _RefCounterMixin):
    async def save(self, profile: IdentityGovernanceProfile) -> None:
        async with session_scope(tenant_id=profile.tenant_id) as session:
            row = await session.get(IgaProfileRow, _uuid(profile.id))
            if row is None:
                session.add(
                    IgaProfileRow(
                        id=_uuid(profile.id),
                        tenant_id=profile.tenant_id,
                        profile_ref=profile.profile_ref,
                        access_review_frequency_days=profile.access_review_frequency_days,
                        certification_required=profile.certification_required,
                        sod_enforcement=profile.sod_enforcement,
                        temporary_access_max_hours=profile.temporary_access_max_hours,
                        emergency_access_max_hours=profile.emergency_access_max_hours,
                        metadata_json=dict(profile.metadata or {}),
                        created_at=profile.created_at,
                    )
                )
            else:
                row.profile_ref = profile.profile_ref
                row.access_review_frequency_days = profile.access_review_frequency_days
                row.certification_required = profile.certification_required
                row.sod_enforcement = profile.sod_enforcement
                row.temporary_access_max_hours = profile.temporary_access_max_hours
                row.emergency_access_max_hours = profile.emergency_access_max_hours
                row.metadata_json = dict(profile.metadata or {})

    async def find_by_tenant(self, tenant_id: str) -> IdentityGovernanceProfile | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(IgaProfileRow).where(IgaProfileRow.tenant_id == tenant_id)
            )
            return _profile_from_row(row) if row else None

    def next_profile_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "ERP-IGP-PRF")


class PostgresAccessRequestRepository(IAccessRequestRepository, _RefCounterMixin):
    async def save(self, request: AccessRequest) -> None:
        async with session_scope(tenant_id=request.tenant_id) as session:
            row = await session.get(IgaAccessRequestRow, _uuid(request.id))
            if row is None:
                session.add(
                    IgaAccessRequestRow(
                        id=_uuid(request.id),
                        tenant_id=request.tenant_id,
                        request_ref=request.request_ref,
                        requester_id=request.requester_id,
                        target_user_id=request.target_user_id,
                        requested_roles=list(request.requested_roles or []),
                        justification=request.justification,
                        status=request.status,
                        approver_id=request.approver_id,
                        sod_checked=request.sod_checked,
                        sod_valid=request.sod_valid,
                        metadata_json=dict(request.metadata or {}),
                        created_at=request.created_at,
                        updated_at=request.updated_at,
                    )
                )
            else:
                row.request_ref = request.request_ref
                row.requester_id = request.requester_id
                row.target_user_id = request.target_user_id
                row.requested_roles = list(request.requested_roles or [])
                row.justification = request.justification
                row.status = request.status
                row.approver_id = request.approver_id
                row.sod_checked = request.sod_checked
                row.sod_valid = request.sod_valid
                row.metadata_json = dict(request.metadata or {})
                row.updated_at = request.updated_at

    async def find_by_ref(self, tenant_id: str, request_ref: str) -> AccessRequest | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(IgaAccessRequestRow).where(
                    IgaAccessRequestRow.tenant_id == tenant_id,
                    IgaAccessRequestRow.request_ref == request_ref,
                )
            )
            return _request_from_row(row) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[AccessRequest]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(IgaAccessRequestRow).where(IgaAccessRequestRow.tenant_id == tenant_id)
                )
            ).all()
        items = [_request_from_row(r) for r in rows]
        return sorted(items, key=lambda r: r.created_at, reverse=True)

    def next_request_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "ERP-ARQ")


class PostgresAccessReviewRepository(IAccessReviewRepository, _RefCounterMixin):
    async def save(self, review: AccessReview) -> None:
        async with session_scope(tenant_id=review.tenant_id) as session:
            row = await session.get(IgaAccessReviewRow, _uuid(review.id))
            if row is None:
                session.add(
                    IgaAccessReviewRow(
                        id=_uuid(review.id),
                        tenant_id=review.tenant_id,
                        review_ref=review.review_ref,
                        title=review.title,
                        reviewer_id=review.reviewer_id,
                        scope_user_ids=list(review.scope_user_ids or []),
                        status=review.status,
                        findings=list(review.findings or []),
                        completed_at=_parse_dt(review.completed_at),
                        metadata_json=dict(review.metadata or {}),
                        created_at=review.created_at,
                    )
                )
            else:
                row.review_ref = review.review_ref
                row.title = review.title
                row.reviewer_id = review.reviewer_id
                row.scope_user_ids = list(review.scope_user_ids or [])
                row.status = review.status
                row.findings = list(review.findings or [])
                row.completed_at = _parse_dt(review.completed_at)
                row.metadata_json = dict(review.metadata or {})

    async def find_by_ref(self, tenant_id: str, review_ref: str) -> AccessReview | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(IgaAccessReviewRow).where(
                    IgaAccessReviewRow.tenant_id == tenant_id,
                    IgaAccessReviewRow.review_ref == review_ref,
                )
            )
            return _review_from_row(row) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[AccessReview]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(IgaAccessReviewRow).where(IgaAccessReviewRow.tenant_id == tenant_id)
                )
            ).all()
        items = [_review_from_row(r) for r in rows]
        return sorted(items, key=lambda r: r.created_at, reverse=True)

    def next_review_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "ERP-ARV")


class PostgresPrivilegeCertificationRepository(IPrivilegeCertificationRepository, _RefCounterMixin):
    async def save(self, certification: PrivilegeCertification) -> None:
        async with session_scope(tenant_id=certification.tenant_id) as session:
            row = await session.get(IgaPrivilegeCertificationRow, _uuid(certification.id))
            if row is None:
                session.add(
                    IgaPrivilegeCertificationRow(
                        id=_uuid(certification.id),
                        tenant_id=certification.tenant_id,
                        certification_ref=certification.certification_ref,
                        user_id=certification.user_id,
                        role_ids=list(certification.role_ids or []),
                        certifier_id=certification.certifier_id,
                        status=certification.status,
                        notes=certification.notes,
                        certified_at=_parse_dt(certification.certified_at),
                        metadata_json=dict(certification.metadata or {}),
                        created_at=certification.created_at,
                    )
                )
            else:
                row.certification_ref = certification.certification_ref
                row.user_id = certification.user_id
                row.role_ids = list(certification.role_ids or [])
                row.certifier_id = certification.certifier_id
                row.status = certification.status
                row.notes = certification.notes
                row.certified_at = _parse_dt(certification.certified_at)
                row.metadata_json = dict(certification.metadata or {})

    async def find_by_ref(self, tenant_id: str, certification_ref: str) -> PrivilegeCertification | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(IgaPrivilegeCertificationRow).where(
                    IgaPrivilegeCertificationRow.tenant_id == tenant_id,
                    IgaPrivilegeCertificationRow.certification_ref == certification_ref,
                )
            )
            return _cert_from_row(row) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[PrivilegeCertification]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(IgaPrivilegeCertificationRow).where(
                        IgaPrivilegeCertificationRow.tenant_id == tenant_id
                    )
                )
            ).all()
        items = [_cert_from_row(r) for r in rows]
        return sorted(items, key=lambda c: c.created_at, reverse=True)

    def next_certification_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "ERP-CERT")


class PostgresTemporaryAccessGrantRepository(ITemporaryAccessGrantRepository, _RefCounterMixin):
    async def save(self, grant: TemporaryAccessGrant) -> None:
        expires = _parse_dt(grant.expires_at) or datetime.now(UTC)
        async with session_scope(tenant_id=grant.tenant_id) as session:
            row = await session.get(IgaTemporaryAccessGrantRow, _uuid(grant.id))
            if row is None:
                session.add(
                    IgaTemporaryAccessGrantRow(
                        id=_uuid(grant.id),
                        tenant_id=grant.tenant_id,
                        grant_ref=grant.grant_ref,
                        user_id=grant.user_id,
                        roles=list(grant.roles or []),
                        granted_by=grant.granted_by,
                        expires_at=expires,
                        status=grant.status,
                        justification=grant.justification,
                        metadata_json=dict(grant.metadata or {}),
                        created_at=grant.created_at,
                    )
                )
            else:
                row.grant_ref = grant.grant_ref
                row.user_id = grant.user_id
                row.roles = list(grant.roles or [])
                row.granted_by = grant.granted_by
                row.expires_at = expires
                row.status = grant.status
                row.justification = grant.justification
                row.metadata_json = dict(grant.metadata or {})

    async def list_by_tenant(self, tenant_id: str) -> list[TemporaryAccessGrant]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(IgaTemporaryAccessGrantRow).where(
                        IgaTemporaryAccessGrantRow.tenant_id == tenant_id
                    )
                )
            ).all()
        items = [_tmp_from_row(r) for r in rows]
        return sorted(items, key=lambda g: g.created_at, reverse=True)

    def next_grant_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "ERP-TMP")


class PostgresEmergencyAccessGrantRepository(IEmergencyAccessGrantRepository, _RefCounterMixin):
    async def save(self, grant: EmergencyAccessGrant) -> None:
        expires = _parse_dt(grant.expires_at) or datetime.now(UTC)
        async with session_scope(tenant_id=grant.tenant_id) as session:
            row = await session.get(IgaEmergencyAccessGrantRow, _uuid(grant.id))
            if row is None:
                session.add(
                    IgaEmergencyAccessGrantRow(
                        id=_uuid(grant.id),
                        tenant_id=grant.tenant_id,
                        grant_ref=grant.grant_ref,
                        user_id=grant.user_id,
                        roles=list(grant.roles or []),
                        granted_by=grant.granted_by,
                        expires_at=expires,
                        status=grant.status,
                        incident_ref=grant.incident_ref,
                        justification=grant.justification,
                        metadata_json=dict(grant.metadata or {}),
                        created_at=grant.created_at,
                    )
                )
            else:
                row.grant_ref = grant.grant_ref
                row.user_id = grant.user_id
                row.roles = list(grant.roles or [])
                row.granted_by = grant.granted_by
                row.expires_at = expires
                row.status = grant.status
                row.incident_ref = grant.incident_ref
                row.justification = grant.justification
                row.metadata_json = dict(grant.metadata or {})

    async def list_by_tenant(self, tenant_id: str) -> list[EmergencyAccessGrant]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(IgaEmergencyAccessGrantRow).where(
                        IgaEmergencyAccessGrantRow.tenant_id == tenant_id
                    )
                )
            ).all()
        items = [_emg_from_row(r) for r in rows]
        return sorted(items, key=lambda g: g.created_at, reverse=True)

    def next_grant_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "ERP-EMG")


class PostgresGovernanceAuditEntryRepository(IGovernanceAuditEntryRepository, _RefCounterMixin):
    async def save(self, entry: GovernanceAuditEntry) -> None:
        async with session_scope(tenant_id=entry.tenant_id) as session:
            row = await session.get(IgaAuditEntryRow, _uuid(entry.id))
            if row is None:
                session.add(
                    IgaAuditEntryRow(
                        id=_uuid(entry.id),
                        tenant_id=entry.tenant_id,
                        entry_ref=entry.entry_ref,
                        action=entry.action,
                        actor_id=entry.actor_id,
                        resource_type=entry.resource_type,
                        resource_ref=entry.resource_ref,
                        details=dict(entry.details or {}),
                        created_at=entry.created_at,
                    )
                )
            else:
                row.entry_ref = entry.entry_ref
                row.action = entry.action
                row.actor_id = entry.actor_id
                row.resource_type = entry.resource_type
                row.resource_ref = entry.resource_ref
                row.details = dict(entry.details or {})

    async def list_by_tenant(self, tenant_id: str) -> list[GovernanceAuditEntry]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(IgaAuditEntryRow).where(IgaAuditEntryRow.tenant_id == tenant_id)
                )
            ).all()
        items = [_audit_from_row(r) for r in rows]
        return sorted(items, key=lambda e: e.created_at, reverse=True)

    def next_entry_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "ERP-IGA")
