"""SQLAlchemy ORM mappings for PostgreSQL repositories."""
from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, Index, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserRow(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "identity"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    display_name: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    locale: Mapped[str] = mapped_column(String(16), nullable=False, default="en-US")
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    mfa_secret: Mapped[str | None] = mapped_column(String(256))
    backup_codes: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    role_ids: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    failed_login_attempts: Mapped[int] = mapped_column(nullable=False, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RoleRow(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "identity"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_system: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    permission_ids: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SessionRow(Base):
    __tablename__ = "sessions"
    __table_args__ = {"schema": "identity"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    refresh_token_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(64))
    user_agent: Mapped[str | None] = mapped_column(Text)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PrincipalRow(Base):
    __tablename__ = "principals"
    __table_args__ = {"schema": "identity"}

    tenant_id: Mapped[str] = mapped_column(String(63), primary_key=True)
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    principal_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    principal_type: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str | None] = mapped_column(String(256))
    display_name: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    partition_bucket: Mapped[int] = mapped_column(Integer, nullable=False)
    principal_metadata: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AccessDecisionRow(Base):
    __tablename__ = "access_decisions"
    __table_args__ = {"schema": "authorization"}

    tenant_id: Mapped[str] = mapped_column(String(63), primary_key=True)
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    decision_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    principal_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    resource: Mapped[str] = mapped_column(String(512), nullable=False, default="")
    action: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    permission_code: Mapped[str | None] = mapped_column(String(256))
    decision: Mapped[str] = mapped_column(String(16), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    context: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class TenantRow(Base):
    __tablename__ = "tenants"
    __table_args__ = {"schema": "tenant"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    slug: Mapped[str] = mapped_column(String(63), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    industry_pack: Mapped[str] = mapped_column(String(64), nullable=False)
    tier: Mapped[str] = mapped_column(String(32), nullable=False, default="professional")
    isolation_strategy: Mapped[str] = mapped_column(String(16), nullable=False, default="row")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="provisioning")
    enabled_modules: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    locale: Mapped[str] = mapped_column(String(16), nullable=False, default="en-US")
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="UTC")
    data_region: Mapped[str] = mapped_column(String(32), nullable=False, default="us-east")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PatientRow(Base):
    __tablename__ = "patients"
    __table_args__ = {"schema": "hospital"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    mrn: Mapped[str] = mapped_column(String(32), nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AdmissionRow(Base):
    __tablename__ = "admissions"
    __table_args__ = {"schema": "hospital"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    patient_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    ward: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    bed_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    admitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    discharged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class BedRow(Base):
    __tablename__ = "beds"
    __table_args__ = {"schema": "hospital"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    ward: Mapped[str] = mapped_column(String(64), nullable=False)
    room: Mapped[str] = mapped_column(String(32), nullable=False)
    bed_code: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="available")
    current_admission_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class EncounterRow(Base):
    __tablename__ = "encounters"
    __table_args__ = {"schema": "hospital"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    patient_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    admission_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="in_progress")
    procedure_codes: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    diagnosis_codes: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class CareEventProjectionRow(Base):
    """Local care timeline — peer IDs + summary only (never lab/pharmacy aggregates)."""

    __tablename__ = "care_event_projections"
    __table_args__ = (
        Index(
            "ix_hospital_care_events_tenant_source",
            "tenant_id",
            "source_event_id",
            unique=True,
        ),
        Index("ix_hospital_care_events_tenant_patient", "tenant_id", "patient_id"),
        Index("ix_hospital_care_events_tenant_encounter", "tenant_id", "encounter_id"),
        Index("ix_hospital_care_events_tenant_occurred", "tenant_id", "occurred_at"),
        {"schema": "hospital"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    source_event_id: Mapped[str] = mapped_column(String(64), nullable=False)
    source_context: Mapped[str] = mapped_column(String(64), nullable=False)
    event_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    peer_id: Mapped[str] = mapped_column(String(64), nullable=False)
    patient_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    admission_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    encounter_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    summary: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    correlation_id: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BillingEncounterRow(Base):
    __tablename__ = "billing_encounters"
    __table_args__ = {"schema": "accounting"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    external_encounter_id: Mapped[str] = mapped_column(String(64), nullable=False)
    patient_ref: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    procedure_codes: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    line_items: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    total_amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    correlation_id: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AccountingInvoiceRow(Base):
    __tablename__ = "invoices"
    __table_args__ = (
        Index("ix_accounting_invoices_tenant", "tenant_id", "status"),
        Index("ix_accounting_invoices_order", "tenant_id", "sales_order_id", unique=True),
        {"schema": "accounting"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    sales_order_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    contact_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    amount: Mapped[object] = mapped_column(Numeric(18, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    line_items: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    correlation_id: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    issued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AccountRow(Base):
    __tablename__ = "accounts"
    __table_args__ = {"schema": "finance"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    code: Mapped[str] = mapped_column(String(16), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    account_type: Mapped[str] = mapped_column(String(32), nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class FiscalPeriodRow(Base):
    __tablename__ = "fiscal_periods"
    __table_args__ = {"schema": "finance"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class JournalEntryRow(Base):
    __tablename__ = "journal_entries"
    __table_args__ = {"schema": "finance"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    external_journal_id: Mapped[str] = mapped_column(String(64), nullable=False)
    source_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_id: Mapped[str] = mapped_column(String(64), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    lines: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    correlation_id: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    posted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class OutboxRow(Base):
    __tablename__ = "outbox"
    __table_args__ = {"schema": "platform"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    event_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    event_name: Mapped[str] = mapped_column(String(256), nullable=False)
    event_version: Mapped[int] = mapped_column(nullable=False, default=1)
    correlation_id: Mapped[str | None] = mapped_column(String(64))
    source_context: Mapped[str | None] = mapped_column(String(64))
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    envelope: Mapped[dict | None] = mapped_column(JSONB)
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    retry_count: Mapped[int] = mapped_column(nullable=False, default=0)
    last_error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProcessedEventRow(Base):
    __tablename__ = "processed_events"
    __table_args__ = {"schema": "platform"}

    tenant_id: Mapped[str] = mapped_column(String(63), primary_key=True)
    event_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    consumer_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    event_name: Mapped[str] = mapped_column(String(256), nullable=False)
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Organization ---


class OrganizationRow(Base):
    __tablename__ = "organizations"
    __table_args__ = {"schema": "organization"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    legal_name: Mapped[str] = mapped_column(String(256), nullable=False)
    root_unit_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class OrgUnitRow(Base):
    __tablename__ = "org_units"
    __table_args__ = {"schema": "organization"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    organization_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    parent_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    unit_type: Mapped[str] = mapped_column(String(32), nullable=False)
    code: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MembershipRow(Base):
    __tablename__ = "memberships"
    __table_args__ = {"schema": "organization"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    org_unit_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    user_id: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Audit ---


class AuditEntryRow(Base):
    __tablename__ = "entries"
    __table_args__ = {"schema": "audit"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    event_name: Mapped[str] = mapped_column(String(128), nullable=False)
    source_context: Mapped[str] = mapped_column(String(64), nullable=False)
    correlation_id: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False)
    resource_id: Mapped[str | None] = mapped_column(String(128))
    actor_id: Mapped[str | None] = mapped_column(String(64))
    severity: Mapped[str] = mapped_column(String(16), nullable=False, default="info")
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AuditExportRow(Base):
    __tablename__ = "exports"
    __table_args__ = {"schema": "audit"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    format: Mapped[str] = mapped_column(String(8), nullable=False)
    filters: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    entry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    data: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    error: Mapped[str | None] = mapped_column(Text)
    requested_by: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class RetentionPolicyRow(Base):
    __tablename__ = "retention_policies"
    __table_args__ = {"schema": "audit"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False, unique=True)
    retention_days: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Documents ---


class FolderRow(Base):
    __tablename__ = "folders"
    __table_args__ = {"schema": "documents"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    parent_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    is_root: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class DocumentRow(Base):
    __tablename__ = "documents"
    __table_args__ = {"schema": "documents"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    folder_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    current_version_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="active")
    doc_metadata: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_by: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class DocumentVersionRow(Base):
    __tablename__ = "document_versions"
    __table_args__ = {"schema": "documents"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    file_name: Mapped[str] = mapped_column(String(256), nullable=False)
    content_type: Mapped[str] = mapped_column(String(128), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    storage_key: Mapped[str | None] = mapped_column(String(256))
    created_by: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SignatureRequestRow(Base):
    __tablename__ = "signature_requests"
    __table_args__ = {"schema": "documents"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    version_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    requester_id: Mapped[str] = mapped_column(String(64), nullable=False)
    signers: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    algorithm: Mapped[str | None] = mapped_column(String(64), nullable=True)
    signature_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_checksum: Mapped[str | None] = mapped_column(String(128), nullable=True)
    key_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


# --- Workflow ---


class ProcessDefinitionRow(Base):
    __tablename__ = "process_definitions"
    __table_args__ = {"schema": "workflow"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    key: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    steps: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProcessInstanceRow(Base):
    __tablename__ = "process_instances"
    __table_args__ = {"schema": "workflow"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    definition_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    definition_key: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    current_step_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    context: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    started_by: Mapped[str] = mapped_column(String(64), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class TaskRow(Base):
    __tablename__ = "tasks"
    __table_args__ = {"schema": "workflow"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    instance_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    step_key: Mapped[str] = mapped_column(String(64), nullable=False)
    step_name: Mapped[str] = mapped_column(String(128), nullable=False)
    assignee_id: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    outcome: Mapped[str | None] = mapped_column(String(16))
    comment: Mapped[str] = mapped_column(Text, nullable=False, default="")
    delegated_from: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


# --- Integration ---


class ConnectorRow(Base):
    __tablename__ = "connectors"
    __table_args__ = {"schema": "integration"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    connector_type: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class WebhookSubscriptionRow(Base):
    __tablename__ = "webhook_subscriptions"
    __table_args__ = {"schema": "integration"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    target_url: Mapped[str] = mapped_column(String(512), nullable=False)
    event_pattern: Mapped[str] = mapped_column(String(128), nullable=False)
    secret: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SyncJobRow(Base):
    __tablename__ = "sync_jobs"
    __table_args__ = {"schema": "integration"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    connector_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    job_type: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    result: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class IntegrationLogRow(Base):
    __tablename__ = "logs"
    __table_args__ = {"schema": "integration"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    log_type: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    reference_id: Mapped[str] = mapped_column(String(64), nullable=False)
    event_name: Mapped[str | None] = mapped_column(String(128))
    detail: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Media ---


class MediaAssetRow(Base):
    __tablename__ = "assets"
    __table_args__ = {"schema": "media"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    file_name: Mapped[str] = mapped_column(String(256), nullable=False)
    content_type: Mapped[str] = mapped_column(String(128), nullable=False)
    media_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    storage_key: Mapped[str | None] = mapped_column(String(512))
    source_ref: Mapped[str | None] = mapped_column(String(256))
    asset_metadata: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_by: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MediaVariantRow(Base):
    __tablename__ = "variants"
    __table_args__ = {"schema": "media"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    asset_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    profile: Mapped[str] = mapped_column(String(32), nullable=False)
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    width: Mapped[int | None] = mapped_column(Integer)
    height: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TranscodeJobRow(Base):
    __tablename__ = "transcode_jobs"
    __table_args__ = {"schema": "media"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    asset_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    profile: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


# --- Analytics ---


class MetricDefinitionRow(Base):
    __tablename__ = "metric_definitions"
    __table_args__ = {"schema": "analytics"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    key: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    event_pattern: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MetricSnapshotRow(Base):
    __tablename__ = "metric_snapshots"
    __table_args__ = {"schema": "analytics"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    metric_key: Mapped[str] = mapped_column(String(64), nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    event_name: Mapped[str | None] = mapped_column(String(128))
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class DashboardRow(Base):
    __tablename__ = "dashboards"
    __table_args__ = {"schema": "analytics"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    widgets: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AlertRuleRow(Base):
    __tablename__ = "alert_rules"
    __table_args__ = {"schema": "analytics"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    metric_key: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    threshold: Mapped[int] = mapped_column(Integer, nullable=False)
    operator: Mapped[str] = mapped_column(String(8), nullable=False, default="gte")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_triggered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Notifications ---


class InboxMessageRow(Base):
    __tablename__ = "inbox_messages"
    __table_args__ = {"schema": "notifications"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    user_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    channel: Mapped[str] = mapped_column(String(32), nullable=False, default="inbox")
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False, default="general")
    source_event: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="unread")
    message_metadata: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class NotificationDeliveryRow(Base):
    __tablename__ = "deliveries"
    __table_args__ = {"schema": "notifications"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    channel: Mapped[str] = mapped_column(String(32), nullable=False)
    recipient: Mapped[str] = mapped_column(String(256), nullable=False)
    template_key: Mapped[str] = mapped_column(String(64), nullable=False)
    source_event: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    error: Mapped[str | None] = mapped_column(Text)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


# --- Settings ---


class TenantSettingsRow(Base):
    __tablename__ = "tenant_settings"
    __table_args__ = {"schema": "settings"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False, unique=True)
    industry_pack: Mapped[str] = mapped_column(String(64), nullable=False)
    config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    features: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    branding: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Search ---


class SearchIndexRow(Base):
    __tablename__ = "indices"
    __table_args__ = {"schema": "search"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    mapping: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    document_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IndexDocumentRow(Base):
    __tablename__ = "documents"
    __table_args__ = {"schema": "search"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    facets: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    source_event: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    indexed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SearchQueryRow(Base):
    __tablename__ = "queries"
    __table_args__ = {"schema": "search"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    query_text: Mapped[str] = mapped_column(String(512), nullable=False)
    entity_types: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    result_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    filters: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ── Clinic bounded context ─────────────────────────────────────────────────


class ClinicPatientRow(Base):
    __tablename__ = "patients"
    __table_args__ = {"schema": "clinic"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    patient_number: Mapped[str] = mapped_column(String(32), nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ClinicAppointmentRow(Base):
    __tablename__ = "appointments"
    __table_args__ = {"schema": "clinic"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    patient_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    provider_name: Mapped[str] = mapped_column(String(128), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ClinicEncounterRow(Base):
    __tablename__ = "encounters"
    __table_args__ = {"schema": "clinic"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    patient_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    appointment_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    diagnosis_codes: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ClinicReferralRow(Base):
    __tablename__ = "referrals"
    __table_args__ = {"schema": "clinic"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    encounter_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    patient_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    target_specialty: Mapped[str] = mapped_column(String(128), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ClinicCareEventProjectionRow(Base):
    """Local ambulatory care timeline — peer IDs + summary only."""

    __tablename__ = "care_event_projections"
    __table_args__ = (
        Index(
            "ix_clinic_care_events_tenant_source",
            "tenant_id",
            "source_event_id",
            unique=True,
        ),
        Index("ix_clinic_care_events_tenant_patient", "tenant_id", "patient_id"),
        Index("ix_clinic_care_events_tenant_encounter", "tenant_id", "encounter_id"),
        Index("ix_clinic_care_events_tenant_occurred", "tenant_id", "occurred_at"),
        {"schema": "clinic"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    source_event_id: Mapped[str] = mapped_column(String(64), nullable=False)
    source_context: Mapped[str] = mapped_column(String(64), nullable=False)
    event_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    peer_id: Mapped[str] = mapped_column(String(64), nullable=False)
    patient_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    encounter_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    summary: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    correlation_id: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ── Municipality bounded context ─────────────────────────────────────────


class MunicipalityPermitRow(Base):
    __tablename__ = "permits"
    __table_args__ = {"schema": "municipality"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    applicant_name: Mapped[str] = mapped_column(String(128), nullable=False)
    permit_type: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    issued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class MunicipalityServiceRequestRow(Base):
    __tablename__ = "service_requests"
    __table_args__ = {"schema": "municipality"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    citizen_name: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class MunicipalityUtilityAccountRow(Base):
    __tablename__ = "utility_accounts"
    __table_args__ = {"schema": "municipality"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    account_number: Mapped[str] = mapped_column(String(32), nullable=False)
    holder_name: Mapped[str] = mapped_column(String(128), nullable=False)
    utility_type: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ── POS bounded context ───────────────────────────────────────────────────


class PosTerminalRow(Base):
    __tablename__ = "terminals"
    __table_args__ = {"schema": "pos"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    terminal_code: Mapped[str] = mapped_column(String(32), nullable=False)
    store_name: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PosShiftRow(Base):
    __tablename__ = "shifts"
    __table_args__ = {"schema": "pos"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    terminal_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    cashier_name: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    total_sales: Mapped[str] = mapped_column(String(32), nullable=False, default="0")
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class PosSaleRow(Base):
    __tablename__ = "sales"
    __table_args__ = {"schema": "pos"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    shift_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    terminal_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    items: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    subtotal: Mapped[str] = mapped_column(String(32), nullable=False)
    tax: Mapped[str] = mapped_column(String(32), nullable=False)
    total: Mapped[str] = mapped_column(String(32), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PosReceiptRow(Base):
    __tablename__ = "receipts"
    __table_args__ = {"schema": "pos"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    sale_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    receipt_number: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


# ── Localization bounded context ───────────────────────────────────────────


class LocalizationLocaleRow(Base):
    __tablename__ = "locales"
    __table_args__ = {"schema": "localization"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    code: Mapped[str] = mapped_column(String(16), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    direction: Mapped[str] = mapped_column(String(8), nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class LocalizationKeyRow(Base):
    __tablename__ = "translation_keys"
    __table_args__ = {"schema": "localization"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    namespace: Mapped[str] = mapped_column(String(64), nullable=False)
    key: Mapped[str] = mapped_column(String(128), nullable=False)
    default_value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class LocalizationBundleRow(Base):
    __tablename__ = "translation_bundles"
    __table_args__ = {"schema": "localization"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    locale_code: Mapped[str] = mapped_column(String(16), nullable=False)
    namespace: Mapped[str] = mapped_column(String(64), nullable=False)
    entries: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Policy ---


class PolicyRow(Base):
    __tablename__ = "policies"
    __table_args__ = {"schema": "policy"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    domain: Mapped[str] = mapped_column(String(32), nullable=False)
    key: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    organization_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PolicyVersionRow(Base):
    __tablename__ = "policy_versions"
    __table_args__ = {"schema": "policy"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    policy_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    conditions: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    rules: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    exceptions: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    approval_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    workflow_key: Mapped[str | None] = mapped_column(String(128))
    require_passing_tests: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cache_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    version_metadata: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- University (CAP-EDU-001) ---


class UniversityStudentRow(Base):
    __tablename__ = "students"
    __table_args__ = {"schema": "university"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    student_number: Mapped[str] = mapped_column(String(32), nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    program_code: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="enrolled")
    identity_user_id: Mapped[str | None] = mapped_column(String(64))
    document_id: Mapped[str | None] = mapped_column(String(64))
    lms_external_id: Mapped[str | None] = mapped_column(String(128))
    lms_provider: Mapped[str | None] = mapped_column(String(64))
    delivery_model: Mapped[str] = mapped_column(String(32), nullable=False, default="degree")
    cohort_ref: Mapped[str | None] = mapped_column(String(64))
    enrolled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UniversityCourseRow(Base):
    __tablename__ = "courses"
    __table_args__ = {"schema": "university"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    course_code: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    credits: Mapped[int] = mapped_column(Integer, nullable=False)
    term: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    lms_external_id: Mapped[str | None] = mapped_column(String(128))
    lms_provider: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UniversityGradeRow(Base):
    __tablename__ = "grades"
    __table_args__ = {"schema": "university"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    student_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    course_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    letter_grade: Mapped[str] = mapped_column(String(8), nullable=False)
    posted_by: Mapped[str | None] = mapped_column(String(64))
    posted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Inventory ---


class InventoryStockLevelRow(Base):
    __tablename__ = "stock_levels"
    __table_args__ = {"schema": "inventory"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    sku: Mapped[str] = mapped_column(String(64), nullable=False)
    quantity_on_hand: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False, default=0)
    quantity_reserved: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Messenger (P5.3 E2EE + LiveKit room refs) ---


class MessengerConversationRow(Base):
    __tablename__ = "conversations"
    __table_args__ = {"schema": "messenger"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    member_ids: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    e2ee_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    livekit_room_name: Mapped[str | None] = mapped_column(String(256))
    meta: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MessengerMessageRow(Base):
    __tablename__ = "messages"
    __table_args__ = {"schema": "messenger"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    conversation_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    sender_id: Mapped[str] = mapped_column(String(64), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    ciphertext: Mapped[str | None] = mapped_column(Text)
    ciphertext_type: Mapped[str | None] = mapped_column(String(64))
    kind: Mapped[str] = mapped_column(String(32), nullable=False, default="text")
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Identity Governance (IGA / P202) ---


class IgaRefCounterRow(Base):
    __tablename__ = "ref_counters"
    __table_args__ = {"schema": "identity_governance"}

    tenant_id: Mapped[str] = mapped_column(String(63), primary_key=True)
    prefix: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class IgaProfileRow(Base):
    __tablename__ = "profiles"
    __table_args__ = {"schema": "identity_governance"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    profile_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    access_review_frequency_days: Mapped[int] = mapped_column(Integer, nullable=False, default=90)
    certification_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sod_enforcement: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    temporary_access_max_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=72)
    emergency_access_max_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IgaAccessRequestRow(Base):
    __tablename__ = "access_requests"
    __table_args__ = {"schema": "identity_governance"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    request_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    requester_id: Mapped[str] = mapped_column(String(128), nullable=False)
    target_user_id: Mapped[str] = mapped_column(String(128), nullable=False)
    requested_roles: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    justification: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    approver_id: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    sod_checked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sod_valid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IgaAccessReviewRow(Base):
    __tablename__ = "access_reviews"
    __table_args__ = {"schema": "identity_governance"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    review_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    reviewer_id: Mapped[str] = mapped_column(String(128), nullable=False)
    scope_user_ids: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    findings: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IgaPrivilegeCertificationRow(Base):
    __tablename__ = "privilege_certifications"
    __table_args__ = {"schema": "identity_governance"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    certification_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False)
    role_ids: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    certifier_id: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=False, default="")
    certified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IgaTemporaryAccessGrantRow(Base):
    __tablename__ = "temporary_access_grants"
    __table_args__ = {"schema": "identity_governance"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    grant_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False)
    roles: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    granted_by: Mapped[str] = mapped_column(String(128), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    justification: Mapped[str] = mapped_column(Text, nullable=False, default="")
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IgaEmergencyAccessGrantRow(Base):
    __tablename__ = "emergency_access_grants"
    __table_args__ = {"schema": "identity_governance"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    grant_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False)
    roles: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    granted_by: Mapped[str] = mapped_column(String(128), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    incident_ref: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    justification: Mapped[str] = mapped_column(Text, nullable=False, default="")
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IgaAuditEntryRow(Base):
    __tablename__ = "audit_entries"
    __table_args__ = {"schema": "identity_governance"}

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    entry_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False)
    resource_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    details: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Secrets (metadata refs only — never plaintext/ciphertext) ---


class SecretMaterialRow(Base):
    __tablename__ = "secret_materials"
    __table_args__ = (
        Index("ix_secrets_materials_tenant_ref", "tenant_id", "secret_ref", unique=True),
        {"schema": "secrets"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    secret_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    connector_id: Mapped[str] = mapped_column(String(64), nullable=False)
    external_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    key_ref: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    rotation_policy_ref: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    provider_catalog_type: Mapped[str] = mapped_column(String(32), nullable=False, default="vault_provider")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Laboratory (CAP-HLT-007) ---


class LaboratoryTestOrderRow(Base):
    __tablename__ = "test_orders"
    __table_args__ = (
        Index("ix_laboratory_test_orders_tenant_number", "tenant_id", "order_number", unique=True),
        Index("ix_laboratory_test_orders_tenant_created", "tenant_id", "created_at"),
        Index("ix_laboratory_test_orders_tenant_patient", "tenant_id", "patient_ref"),
        {"schema": "laboratory"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    order_number: Mapped[str] = mapped_column(String(64), nullable=False)
    patient_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    test_code: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="ordered")
    result_value: Mapped[str | None] = mapped_column(String(256))
    result_unit: Mapped[str | None] = mapped_column(String(64))
    source_encounter_ref: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finalized_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class LaboratorySampleRow(Base):
    __tablename__ = "samples"
    __table_args__ = (
        Index("ix_laboratory_samples_tenant_accession", "tenant_id", "accession_number", unique=True),
        Index("ix_laboratory_samples_tenant_order", "tenant_id", "order_id"),
        Index("ix_laboratory_samples_tenant_received", "tenant_id", "received_at"),
        {"schema": "laboratory"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    order_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    accession_number: Mapped[str] = mapped_column(String(64), nullable=False)
    specimen_type: Mapped[str] = mapped_column(String(64), nullable=False)
    patient_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Pharmacy (CAP-HLT-008) ---


class PharmacyPrescriptionRow(Base):
    __tablename__ = "prescriptions"
    __table_args__ = (
        Index("ix_pharmacy_prescriptions_tenant_rx", "tenant_id", "rx_number", unique=True),
        Index("ix_pharmacy_prescriptions_tenant_created", "tenant_id", "created_at"),
        Index("ix_pharmacy_prescriptions_tenant_patient", "tenant_id", "patient_ref"),
        {"schema": "pharmacy"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    rx_number: Mapped[str] = mapped_column(String(64), nullable=False)
    patient_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    drug_code: Mapped[str] = mapped_column(String(64), nullable=False)
    drug_name: Mapped[str] = mapped_column(String(256), nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="received")
    source_encounter_ref: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PharmacyDispenseRecordRow(Base):
    __tablename__ = "dispense_records"
    __table_args__ = (
        Index("ix_pharmacy_dispenses_tenant_rx", "tenant_id", "prescription_id"),
        Index("ix_pharmacy_dispenses_tenant_dispensed", "tenant_id", "dispensed_at"),
        {"schema": "pharmacy"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    prescription_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    patient_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    drug_code: Mapped[str] = mapped_column(String(64), nullable=False)
    quantity_dispensed: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    dispensed_by: Mapped[str | None] = mapped_column(String(128))
    dispensed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# --- Financial Kernel money-path (GL) — CAP financial kernel ---


class FinancialKernelChartOfAccountRow(Base):
    __tablename__ = "chart_of_accounts"
    __table_args__ = (
        Index("ix_fk_coa_tenant_code", "tenant_id", "code", unique=True),
        Index("ix_fk_coa_tenant_key", "tenant_id", "account_key"),
        {"schema": "financial_kernel"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    account_key: Mapped[str | None] = mapped_column(String(128))
    parent_account_id: Mapped[str | None] = mapped_column(String(64))
    tree_id: Mapped[str | None] = mapped_column(String(64))
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class FinancialKernelJournalRow(Base):
    __tablename__ = "journals"
    __table_args__ = (
        Index("ix_fk_journals_tenant_idemp", "tenant_id", "idempotency_key", unique=True),
        Index("ix_fk_journals_tenant_posted", "tenant_id", "posted_at"),
        {"schema": "financial_kernel"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    period_id: Mapped[str | None] = mapped_column(String(64))
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class FinancialKernelFiscalYearRow(Base):
    __tablename__ = "fiscal_years"
    __table_args__ = (
        Index("ix_fk_fy_tenant", "tenant_id"),
        {"schema": "financial_kernel"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class FinancialKernelFiscalPeriodRow(Base):
    __tablename__ = "fiscal_periods"
    __table_args__ = (
        Index("ix_fk_fp_tenant_status", "tenant_id", "status"),
        Index("ix_fk_fp_tenant_year", "tenant_id", "fiscal_year_id"),
        {"schema": "financial_kernel"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    fiscal_year_id: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    organization_id: Mapped[str | None] = mapped_column(String(64))
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


# --- Banking money-path ---


class BankingCustomerRow(Base):
    __tablename__ = "customers"
    __table_args__ = (
        Index("ix_banking_customers_tenant_email", "tenant_id", "email", unique=True),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BankingAccountProductRow(Base):
    __tablename__ = "account_products"
    __table_args__ = (
        Index("ix_banking_products_tenant_code", "tenant_id", "product_code", unique=True),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    product_code: Mapped[str] = mapped_column(String(64), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class BankingAccountRow(Base):
    __tablename__ = "accounts"
    __table_args__ = (
        Index("ix_banking_accounts_tenant_number", "tenant_id", "account_number", unique=True),
        Index("ix_banking_accounts_tenant_customer", "tenant_id", "customer_id"),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    customer_id: Mapped[str] = mapped_column(String(64), nullable=False)
    account_number: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BankingPaymentTransferRow(Base):
    __tablename__ = "payment_transfers"
    __table_args__ = (
        Index("ix_banking_transfers_tenant_ref", "tenant_id", "transfer_ref", unique=True),
        Index("ix_banking_transfers_tenant_status", "tenant_id", "status"),
        Index("ix_banking_transfers_batch", "batch_id"),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    transfer_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    source_account_id: Mapped[str] = mapped_column(String(64), nullable=False)
    customer_id: Mapped[str] = mapped_column(String(64), nullable=False)
    batch_id: Mapped[str | None] = mapped_column(String(64))
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BankingDepositProfileRow(Base):
    __tablename__ = "deposit_profiles"
    __table_args__ = (
        Index("ix_banking_deposit_profiles_tenant_account", "tenant_id", "account_id"),
        Index("ix_banking_deposit_profiles_tenant_customer", "tenant_id", "customer_id"),
        Index("ix_banking_deposit_profiles_tenant_status", "tenant_id", "status"),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    account_id: Mapped[str] = mapped_column(String(64), nullable=False)
    customer_id: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending_approval")
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BankingDepositTransactionRow(Base):
    __tablename__ = "deposit_transactions"
    __table_args__ = (
        Index("ix_banking_deposit_tx_tenant_ref", "tenant_id", "transaction_ref", unique=True),
        Index("ix_banking_deposit_tx_deposit", "tenant_id", "deposit_id"),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    deposit_id: Mapped[str] = mapped_column(String(64), nullable=False)
    transaction_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class BankingDepositAccrualRow(Base):
    __tablename__ = "deposit_accruals"
    __table_args__ = (
        Index("ix_banking_deposit_accruals_deposit", "tenant_id", "deposit_id"),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    deposit_id: Mapped[str] = mapped_column(String(64), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class BankingProfitRuleRow(Base):
    __tablename__ = "profit_rules"
    __table_args__ = (
        Index("ix_banking_profit_rules_tenant_code", "tenant_id", "rule_code", unique=True),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    rule_code: Mapped[str] = mapped_column(String(64), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class BankingLoanProfileRow(Base):
    __tablename__ = "loan_profiles"
    __table_args__ = (
        Index("ix_banking_loan_profiles_tenant_ref", "tenant_id", "loan_ref", unique=True),
        Index("ix_banking_loan_profiles_tenant_account", "tenant_id", "account_id"),
        Index("ix_banking_loan_profiles_tenant_status", "tenant_id", "status"),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    account_id: Mapped[str] = mapped_column(String(64), nullable=False)
    loan_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BankingLoanTransactionRow(Base):
    __tablename__ = "loan_transactions"
    __table_args__ = (
        Index("ix_banking_loan_tx_tenant_ref", "tenant_id", "transaction_ref", unique=True),
        Index("ix_banking_loan_tx_loan", "tenant_id", "loan_id"),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    loan_id: Mapped[str] = mapped_column(String(64), nullable=False)
    transaction_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class BankingLoanInstallmentRow(Base):
    __tablename__ = "loan_installments"
    __table_args__ = (
        Index("ix_banking_loan_installments_loan", "tenant_id", "loan_id"),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    loan_id: Mapped[str] = mapped_column(String(64), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class BankingLoanCollateralRow(Base):
    __tablename__ = "loan_collaterals"
    __table_args__ = (
        Index("ix_banking_loan_collaterals_loan", "tenant_id", "loan_id"),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    loan_id: Mapped[str] = mapped_column(String(64), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class BankingLoanGuarantorRow(Base):
    __tablename__ = "loan_guarantors"
    __table_args__ = (
        Index("ix_banking_loan_guarantors_loan", "tenant_id", "loan_id"),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    loan_id: Mapped[str] = mapped_column(String(64), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class BankingLoanCreditRiskRow(Base):
    __tablename__ = "loan_credit_risks"
    __table_args__ = (
        Index("ix_banking_loan_credit_risks_loan", "tenant_id", "loan_id"),
        {"schema": "banking"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    loan_id: Mapped[str] = mapped_column(String(64), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


# --- Treasury money-path ---


class TreasuryAccountRow(Base):
    __tablename__ = "accounts"
    __table_args__ = (
        Index("ix_treasury_accounts_tenant_code", "tenant_id", "code", unique=True),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    account_type: Mapped[str] = mapped_column(String(32), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TreasuryTransferRow(Base):
    __tablename__ = "transfers"
    __table_args__ = (
        Index("ix_treasury_transfers_tenant_ref", "tenant_id", "reference", unique=True),
        Index("ix_treasury_transfers_tenant_status", "tenant_id", "status"),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    reference: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    from_account_id: Mapped[str] = mapped_column(String(64), nullable=False)
    to_account_id: Mapped[str] = mapped_column(String(64), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TreasuryCashLocationRow(Base):
    __tablename__ = "cash_locations"
    __table_args__ = (
        Index("ix_treasury_cash_loc_tenant_code", "tenant_id", "code", unique=True),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TreasuryCashTransactionRow(Base):
    __tablename__ = "cash_transactions"
    __table_args__ = (
        Index("ix_treasury_cash_tx_location", "tenant_id", "location_id"),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    location_id: Mapped[str] = mapped_column(String(64), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(32), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TreasuryBankAccountRow(Base):
    __tablename__ = "bank_accounts"
    __table_args__ = (
        Index("ix_treasury_bank_accounts_tenant_code", "tenant_id", "code", unique=True),
        Index("ix_treasury_bank_accounts_bank", "tenant_id", "bank_id"),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    bank_id: Mapped[str] = mapped_column(String(64), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TreasuryCashPoolRow(Base):
    __tablename__ = "cash_pools"
    __table_args__ = (
        Index("ix_treasury_cash_pools_tenant_code", "tenant_id", "code", unique=True),
        Index("ix_treasury_cash_pools_tenant_status", "tenant_id", "status"),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class TreasuryLiquiditySnapshotRow(Base):
    __tablename__ = "liquidity_snapshots"
    __table_args__ = (
        Index("ix_treasury_liquidity_snapshots_tenant_period_date", "tenant_id", "period_type", "as_of_date"),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    period_type: Mapped[str] = mapped_column(String(32), nullable=False)
    as_of_date: Mapped[str] = mapped_column(String(32), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class TreasuryFundingNeedRow(Base):
    __tablename__ = "funding_needs"
    __table_args__ = (
        Index("ix_treasury_funding_needs_tenant_status", "tenant_id", "status"),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class TreasuryBankStatementImportRow(Base):
    __tablename__ = "bank_statement_imports"
    __table_args__ = (
        Index("ix_treasury_bank_statement_imports_account", "tenant_id", "treasury_account_id", "status"),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    treasury_account_id: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="imported")
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class TreasuryBankReconciliationRow(Base):
    __tablename__ = "bank_reconciliations"
    __table_args__ = (
        Index("ix_treasury_bank_reconciliations_account", "tenant_id", "treasury_account_id", "status"),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    treasury_account_id: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class TreasuryBankReconciliationAuditRow(Base):
    __tablename__ = "bank_reconciliation_audits"
    __table_args__ = (
        Index("ix_treasury_bank_reconciliation_audits_reconciliation", "tenant_id", "reconciliation_id"),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    reconciliation_id: Mapped[str] = mapped_column(String(64), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class TreasuryCashReconciliationRunRow(Base):
    __tablename__ = "cash_reconciliation_runs"
    __table_args__ = (
        Index("ix_treasury_cash_reconciliation_runs_location", "tenant_id", "location_id", "status"),
        Index("ix_treasury_cash_reconciliation_runs_branch", "tenant_id", "branch_id"),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    location_id: Mapped[str] = mapped_column(String(64), nullable=False)
    branch_id: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class TreasuryCashReconciliationAuditRow(Base):
    __tablename__ = "cash_reconciliation_audits"
    __table_args__ = (
        Index("ix_treasury_cash_reconciliation_audits_reconciliation", "tenant_id", "reconciliation_id"),
        {"schema": "treasury"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    reconciliation_id: Mapped[str] = mapped_column(String(64), nullable=False)
    document: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


# --- Identity Federation (EIFTP SoR) ---


class FederationIdentityProviderRow(Base):
    __tablename__ = "identity_providers"
    __table_args__ = (
        Index("uq_federation_idp_tenant_ref", "tenant_id", "provider_ref", unique=True),
        {"schema": "federation"},
    )

    tenant_id: Mapped[str] = mapped_column(String(63), primary_key=True)
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    provider_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    protocol: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    plugin_id: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class FederationTrustRelationshipRow(Base):
    __tablename__ = "trust_relationships"
    __table_args__ = (
        Index("uq_federation_trust_ref", "tenant_id", "trust_ref", unique=True),
        {"schema": "federation"},
    )

    tenant_id: Mapped[str] = mapped_column(String(63), primary_key=True)
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    trust_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    source_entity_type: Mapped[str] = mapped_column(String(32), nullable=False)
    source_entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
    target_entity_type: Mapped[str] = mapped_column(String(32), nullable=False)
    target_entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
    trust_score: Mapped[int] = mapped_column(Integer, nullable=False, default=50)
    trust_level: Mapped[str] = mapped_column(String(16), nullable=False, default="medium")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    valid_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class FederationClaimsMappingRow(Base):
    __tablename__ = "claims_mappings"
    __table_args__ = (
        Index("uq_federation_claims_ref", "tenant_id", "mapping_ref", unique=True),
        {"schema": "federation"},
    )

    tenant_id: Mapped[str] = mapped_column(String(63), primary_key=True)
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    mapping_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    source_claim: Mapped[str] = mapped_column(String(128), nullable=False)
    target_claim: Mapped[str] = mapped_column(String(128), nullable=False)
    transform_type: Mapped[str] = mapped_column(String(32), nullable=False, default="direct")
    transform_config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class FederationIdentityLinkRow(Base):
    __tablename__ = "identity_links"
    __table_args__ = (
        Index("uq_federation_link_ref", "tenant_id", "link_ref", unique=True),
        Index("uq_federation_link_external", "tenant_id", "provider_id", "external_subject", unique=True),
        {"schema": "federation"},
    )

    tenant_id: Mapped[str] = mapped_column(String(63), primary_key=True)
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    link_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    provider_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    external_subject: Mapped[str] = mapped_column(String(256), nullable=False)
    link_status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    linked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)


class FederationSessionRow(Base):
    __tablename__ = "federation_sessions"
    __table_args__ = (
        Index("ix_federation_sessions_ref", "tenant_id", "session_ref"),
        {"schema": "federation"},
    )

    tenant_id: Mapped[str] = mapped_column(String(63), primary_key=True)
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    session_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    user_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    provider_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    protocol: Mapped[str] = mapped_column(String(32), nullable=False)
    idp_session_id: Mapped[str | None] = mapped_column(String(256))
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class FederationRefCounterRow(Base):
    __tablename__ = "ref_counters"
    __table_args__ = {"schema": "federation"}

    tenant_id: Mapped[str] = mapped_column(String(63), primary_key=True)
    prefix: Mapped[str] = mapped_column(String(64), primary_key=True)
    next_value: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


# ── CRM bounded context (CAP-ENT-001) ──────────────────────────────────────


class CrmContactRow(Base):
    __tablename__ = "contacts"
    __table_args__ = (
        Index("ix_crm_contacts_tenant_email", "tenant_id", "email", unique=True),
        {"schema": "crm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    company: Mapped[str | None] = mapped_column(String(128))
    phone: Mapped[str | None] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CrmOpportunityRow(Base):
    __tablename__ = "opportunities"
    __table_args__ = (
        Index("ix_crm_opportunities_tenant", "tenant_id", "stage"),
        {"schema": "crm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    contact_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    amount: Mapped[object] = mapped_column(Numeric(18, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    stage: Mapped[str] = mapped_column(String(32), nullable=False, default="qualifying")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class SalesQuotationRow(Base):
    __tablename__ = "quotations"
    __table_args__ = (
        Index("ix_sales_quotations_tenant", "tenant_id", "status"),
        Index("ix_sales_quotations_opportunity", "tenant_id", "opportunity_id"),
        {"schema": "sales"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    contact_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    opportunity_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    amount: Mapped[object] = mapped_column(Numeric(18, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class SalesOrderRow(Base):
    __tablename__ = "orders"
    __table_args__ = (
        Index("ix_sales_orders_tenant", "tenant_id", "status"),
        {"schema": "sales"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    contact_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    quotation_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    opportunity_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    amount: Mapped[object] = mapped_column(Numeric(18, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="confirmed")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProcurementRequisitionRow(Base):
    __tablename__ = "requisitions"
    __table_args__ = (
        Index("ix_procurement_requisitions_tenant", "tenant_id", "status"),
        {"schema": "procurement"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(63), nullable=False)
    sku: Mapped[str] = mapped_column(String(64), nullable=False)
    quantity: Mapped[object] = mapped_column(Numeric(18, 4), nullable=False)
    quantity_available: Mapped[object] = mapped_column(Numeric(18, 4), nullable=False)
    reorder_threshold: Mapped[object] = mapped_column(Numeric(18, 4), nullable=False)
    stock_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    reason: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    correlation_id: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
