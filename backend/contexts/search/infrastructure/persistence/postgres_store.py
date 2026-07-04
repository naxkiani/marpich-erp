"""PostgreSQL repositories — Search bounded context."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import delete, func, select

from contexts.search.domain.aggregates.index_document import IndexDocument
from contexts.search.domain.aggregates.search_index import SearchIndex
from contexts.search.domain.aggregates.search_query import SearchQuery
from contexts.search.domain.ports.repositories import (
    IIndexDocumentRepository,
    ISearchIndexRepository,
    ISearchQueryRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import IndexDocumentRow, SearchIndexRow, SearchQueryRow


class PostgresSearchIndexRepository(ISearchIndexRepository):
    async def save(self, index: SearchIndex) -> None:
        async with session_scope() as session:
            row = await session.scalar(
                select(SearchIndexRow).where(
                    SearchIndexRow.tenant_id == index.tenant_id,
                    SearchIndexRow.entity_type == index.entity_type,
                )
            )
            if row is None:
                session.add(
                    SearchIndexRow(
                        id=UUID(str(index.id)),
                        tenant_id=index.tenant_id,
                        entity_type=index.entity_type,
                        is_active=index.is_active,
                        mapping=index.mapping,
                        document_count=index.document_count,
                        created_at=index.created_at,
                    )
                )
            else:
                row.is_active = index.is_active
                row.mapping = index.mapping
                row.document_count = index.document_count

    async def find_by_type(self, tenant_id: str, entity_type: str) -> SearchIndex | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(SearchIndexRow).where(
                    SearchIndexRow.tenant_id == tenant_id,
                    SearchIndexRow.entity_type == entity_type.lower(),
                )
            )
            return _index_from_row(row) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[SearchIndex]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(SearchIndexRow).where(SearchIndexRow.tenant_id == tenant_id)
                )
            ).all()
        return [_index_from_row(r) for r in rows]


class PostgresIndexDocumentRepository(IIndexDocumentRepository):
    async def upsert(self, document: IndexDocument) -> None:
        async with session_scope() as session:
            row = await session.scalar(
                select(IndexDocumentRow).where(
                    IndexDocumentRow.tenant_id == document.tenant_id,
                    IndexDocumentRow.entity_type == document.entity_type,
                    IndexDocumentRow.entity_id == document.entity_id,
                )
            )
            if row is None:
                session.add(
                    IndexDocumentRow(
                        id=UUID(str(document.id)),
                        tenant_id=document.tenant_id,
                        entity_type=document.entity_type,
                        entity_id=document.entity_id,
                        title=document.title,
                        body=document.body,
                        facets=document.facets,
                        source_event=document.source_event,
                        indexed_at=document.indexed_at,
                    )
                )
            else:
                row.title = document.title
                row.body = document.body
                row.facets = document.facets
                row.source_event = document.source_event
                row.indexed_at = document.indexed_at

    async def search(
        self,
        tenant_id: str,
        query: str,
        *,
        entity_types: list[str] | None = None,
        limit: int = 50,
    ) -> list[IndexDocument]:
        async with session_scope() as session:
            stmt = select(IndexDocumentRow).where(IndexDocumentRow.tenant_id == tenant_id)
            if entity_types:
                stmt = stmt.where(
                    IndexDocumentRow.entity_type.in_([t.lower() for t in entity_types])
                )
            rows = (await session.scalars(stmt.order_by(IndexDocumentRow.indexed_at.desc()))).all()
        docs = [_document_from_row(r) for r in rows if _document_from_row(r).matches_query(query)]
        return docs[:limit]

    async def suggest(self, tenant_id: str, prefix: str, *, limit: int = 10) -> list[str]:
        needle = prefix.lower().strip()
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(IndexDocumentRow)
                    .where(IndexDocumentRow.tenant_id == tenant_id)
                    .order_by(IndexDocumentRow.indexed_at.desc())
                    .limit(200)
                )
            ).all()
        titles = [
            row.title
            for row in rows
            if not needle or row.title.lower().startswith(needle)
        ]
        return sorted(set(titles))[:limit]

    async def count_by_tenant(self, tenant_id: str) -> int:
        async with session_scope() as session:
            return await session.scalar(
                select(func.count())
                .select_from(IndexDocumentRow)
                .where(IndexDocumentRow.tenant_id == tenant_id)
            ) or 0

    async def clear_tenant(self, tenant_id: str) -> int:
        async with session_scope() as session:
            result = await session.execute(
                delete(IndexDocumentRow).where(IndexDocumentRow.tenant_id == tenant_id)
            )
            return result.rowcount


class PostgresSearchQueryRepository(ISearchQueryRepository):
    async def append(self, query: SearchQuery) -> None:
        async with session_scope() as session:
            session.add(
                SearchQueryRow(
                    id=UUID(str(query.id)),
                    tenant_id=query.tenant_id,
                    query_text=query.query_text,
                    entity_types=query.entity_types,
                    result_count=query.result_count,
                    filters=query.filters,
                    created_at=query.created_at,
                )
            )


def _index_from_row(row: SearchIndexRow) -> SearchIndex:
    return SearchIndex(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        entity_type=row.entity_type,
        is_active=row.is_active,
        mapping=row.mapping,
        document_count=row.document_count,
        created_at=row.created_at,
    )


def _document_from_row(row: IndexDocumentRow) -> IndexDocument:
    return IndexDocument(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        entity_type=row.entity_type,
        entity_id=row.entity_id,
        title=row.title,
        body=row.body,
        facets=row.facets,
        source_event=row.source_event,
        indexed_at=row.indexed_at,
    )
