"""PostgreSQL repositories — Messenger (E2EE ciphertext + LiveKit room refs)."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.messenger.domain.aggregates.conversation import Conversation
from contexts.messenger.domain.aggregates.message import Message
from contexts.messenger.domain.ports.repositories import IConversationRepository, IMessageRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import MessengerConversationRow, MessengerMessageRow


class PostgresConversationRepository(IConversationRepository):
    async def save(self, conversation: Conversation) -> None:
        async with session_scope() as session:
            row = await session.get(MessengerConversationRow, UUID(str(conversation.id)))
            if row is None:
                session.add(
                    MessengerConversationRow(
                        id=UUID(str(conversation.id)),
                        tenant_id=conversation.tenant_id,
                        title=conversation.title,
                        member_ids=list(conversation.member_ids),
                        e2ee_enabled=conversation.e2ee_enabled,
                        livekit_room_name=conversation.livekit_room_name,
                        created_at=conversation.created_at,
                    )
                )
            else:
                row.title = conversation.title
                row.member_ids = list(conversation.member_ids)
                row.e2ee_enabled = conversation.e2ee_enabled
                row.livekit_room_name = conversation.livekit_room_name

    async def find_by_id(self, tenant_id: str, conversation_id: UniqueId) -> Conversation | None:
        async with session_scope() as session:
            row = await session.get(MessengerConversationRow, UUID(str(conversation_id)))
            return _conversation_from_row(row) if row and row.tenant_id == tenant_id else None


class PostgresMessageRepository(IMessageRepository):
    async def save(self, message: Message) -> None:
        async with session_scope() as session:
            row = await session.get(MessengerMessageRow, UUID(str(message.id)))
            if row is None:
                session.add(
                    MessengerMessageRow(
                        id=UUID(str(message.id)),
                        tenant_id=message.tenant_id,
                        conversation_id=UUID(str(message.conversation_id)),
                        sender_id=message.sender_id,
                        body=message.body,
                        ciphertext=message.ciphertext,
                        ciphertext_type=message.ciphertext_type,
                        created_at=message.created_at,
                    )
                )
            else:
                row.body = message.body
                row.ciphertext = message.ciphertext
                row.ciphertext_type = message.ciphertext_type

    async def list_by_conversation(
        self, tenant_id: str, conversation_id: UniqueId, *, limit: int = 50
    ) -> list[Message]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(MessengerMessageRow)
                    .where(
                        MessengerMessageRow.tenant_id == tenant_id,
                        MessengerMessageRow.conversation_id == UUID(str(conversation_id)),
                    )
                    .order_by(MessengerMessageRow.created_at.asc())
                )
            ).all()
        return [_message_from_row(r) for r in rows[-limit:]]


def _conversation_from_row(row: MessengerConversationRow) -> Conversation:
    return Conversation(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        title=row.title,
        member_ids=list(row.member_ids or []),
        e2ee_enabled=bool(row.e2ee_enabled),
        livekit_room_name=row.livekit_room_name,
        created_at=row.created_at,
    )


def _message_from_row(row: MessengerMessageRow) -> Message:
    return Message(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        conversation_id=UniqueId.from_string(str(row.conversation_id)),
        sender_id=row.sender_id,
        body=row.body or "",
        ciphertext=row.ciphertext,
        ciphertext_type=row.ciphertext_type,
        created_at=row.created_at,
    )
