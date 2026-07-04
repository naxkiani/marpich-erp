"""PostgreSQL repositories — Integration bounded context."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import or_, select

from contexts.integration.domain.aggregates.connector import Connector, ConnectorType
from contexts.integration.domain.aggregates.integration_log import IntegrationLog, LogStatus
from contexts.integration.domain.aggregates.sync_job import SyncJob, SyncStatus
from contexts.integration.domain.aggregates.webhook_subscription import WebhookSubscription
from contexts.integration.domain.ports.repositories import (
    IConnectorRepository,
    IIntegrationLogRepository,
    ISyncJobRepository,
    IWebhookRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    ConnectorRow,
    IntegrationLogRow,
    SyncJobRow,
    WebhookSubscriptionRow,
)


class PostgresConnectorRepository(IConnectorRepository):
    async def save(self, connector: Connector) -> None:
        async with session_scope() as session:
            row = await session.get(ConnectorRow, UUID(str(connector.id)))
            if row is None:
                session.add(
                    ConnectorRow(
                        id=UUID(str(connector.id)),
                        tenant_id=connector.tenant_id,
                        connector_type=connector.connector_type.value,
                        name=connector.name,
                        config=connector.config,
                        is_active=connector.is_active,
                        created_at=connector.created_at,
                    )
                )
            else:
                row.name = connector.name
                row.config = connector.config
                row.is_active = connector.is_active

    async def find_by_id(self, tenant_id: str, connector_id: UniqueId) -> Connector | None:
        async with session_scope() as session:
            row = await session.get(ConnectorRow, UUID(str(connector_id)))
            if row and row.tenant_id == tenant_id:
                return _connector_from_row(row)
            return None

    async def list_by_tenant(self, tenant_id: str) -> list[Connector]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(ConnectorRow).where(ConnectorRow.tenant_id == tenant_id)
                )
            ).all()
        return [_connector_from_row(r) for r in rows]


class PostgresWebhookRepository(IWebhookRepository):
    async def save(self, webhook: WebhookSubscription) -> None:
        async with session_scope() as session:
            row = await session.get(WebhookSubscriptionRow, UUID(str(webhook.id)))
            if row is None:
                session.add(
                    WebhookSubscriptionRow(
                        id=UUID(str(webhook.id)),
                        tenant_id=webhook.tenant_id,
                        target_url=webhook.target_url,
                        event_pattern=webhook.event_pattern,
                        secret=webhook.secret,
                        description=webhook.description,
                        is_active=webhook.is_active,
                        created_at=webhook.created_at,
                    )
                )
            else:
                row.target_url = webhook.target_url
                row.event_pattern = webhook.event_pattern
                row.secret = webhook.secret
                row.description = webhook.description
                row.is_active = webhook.is_active

    async def find_by_id(self, tenant_id: str, webhook_id: UniqueId) -> WebhookSubscription | None:
        async with session_scope() as session:
            row = await session.get(WebhookSubscriptionRow, UUID(str(webhook_id)))
            if row and row.tenant_id == tenant_id:
                return _webhook_from_row(row)
            return None

    async def list_by_tenant(self, tenant_id: str) -> list[WebhookSubscription]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(WebhookSubscriptionRow).where(WebhookSubscriptionRow.tenant_id == tenant_id)
                )
            ).all()
        return [_webhook_from_row(r) for r in rows]

    async def list_active_for_event(
        self, tenant_id: str, event_name: str
    ) -> list[WebhookSubscription]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(WebhookSubscriptionRow).where(
                        WebhookSubscriptionRow.tenant_id == tenant_id,
                        WebhookSubscriptionRow.is_active.is_(True),
                        or_(
                            WebhookSubscriptionRow.event_pattern == "*",
                            WebhookSubscriptionRow.event_pattern == event_name,
                        ),
                    )
                )
            ).all()
        return [_webhook_from_row(r) for r in rows]


class PostgresSyncJobRepository(ISyncJobRepository):
    async def save(self, job: SyncJob) -> None:
        async with session_scope() as session:
            row = await session.get(SyncJobRow, UUID(str(job.id)))
            if row is None:
                session.add(
                    SyncJobRow(
                        id=UUID(str(job.id)),
                        tenant_id=job.tenant_id,
                        connector_id=UUID(str(job.connector_id)),
                        job_type=job.job_type,
                        status=job.status.value,
                        result=job.result,
                        error=job.error,
                        created_at=job.created_at,
                        completed_at=job.completed_at,
                    )
                )
            else:
                row.status = job.status.value
                row.result = job.result
                row.error = job.error
                row.completed_at = job.completed_at

    async def find_by_id(self, tenant_id: str, job_id: UniqueId) -> SyncJob | None:
        async with session_scope() as session:
            row = await session.get(SyncJobRow, UUID(str(job_id)))
            if row and row.tenant_id == tenant_id:
                return _sync_job_from_row(row)
            return None


class PostgresIntegrationLogRepository(IIntegrationLogRepository):
    async def append(self, log: IntegrationLog) -> None:
        async with session_scope() as session:
            session.add(
                IntegrationLogRow(
                    id=UUID(str(log.id)),
                    tenant_id=log.tenant_id,
                    log_type=log.log_type,
                    status=log.status.value,
                    reference_id=log.reference_id,
                    event_name=log.event_name,
                    detail=log.detail,
                    created_at=log.created_at,
                )
            )

    async def list_by_tenant(self, tenant_id: str, limit: int = 100) -> list[IntegrationLog]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(IntegrationLogRow)
                    .where(IntegrationLogRow.tenant_id == tenant_id)
                    .order_by(IntegrationLogRow.created_at.desc())
                    .limit(limit)
                )
            ).all()
        return [_log_from_row(r) for r in reversed(rows)]


def _connector_from_row(row: ConnectorRow) -> Connector:
    return Connector(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        connector_type=ConnectorType(row.connector_type),
        name=row.name,
        config=row.config,
        is_active=row.is_active,
        created_at=row.created_at,
    )


def _webhook_from_row(row: WebhookSubscriptionRow) -> WebhookSubscription:
    return WebhookSubscription(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        target_url=row.target_url,
        event_pattern=row.event_pattern,
        secret=row.secret,
        description=row.description,
        is_active=row.is_active,
        created_at=row.created_at,
    )


def _sync_job_from_row(row: SyncJobRow) -> SyncJob:
    return SyncJob(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        connector_id=UniqueId(str(row.connector_id)),
        job_type=row.job_type,
        status=SyncStatus(row.status),
        result=row.result,
        error=row.error,
        created_at=row.created_at,
        completed_at=row.completed_at,
    )


def _log_from_row(row: IntegrationLogRow) -> IntegrationLog:
    return IntegrationLog(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        log_type=row.log_type,
        status=LogStatus(row.status),
        reference_id=row.reference_id,
        event_name=row.event_name,
        detail=row.detail,
        created_at=row.created_at,
    )
