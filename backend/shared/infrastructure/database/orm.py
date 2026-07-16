"""SQLAlchemy ORM mappings for PostgreSQL repositories."""
from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, Integer, Numeric, String, Text, func
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
    admitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


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
    connector_type: Mapped[str] = mapped_column(String(16), nullable=False)
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
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
