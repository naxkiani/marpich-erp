"""Messenger application service."""
from __future__ import annotations

from contexts.messenger.domain.aggregates.conversation import Conversation
from contexts.messenger.domain.aggregates.message import Message
from contexts.messenger.domain.events.integration_events import (
    ConversationOpenedIntegration,
    MessageSentIntegration,
)
from contexts.messenger.domain.ports.repositories import IConversationRepository, IMessageRepository
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class MessengerApplicationService:
    def __init__(
        self,
        conversations: IConversationRepository,
        messages: IMessageRepository,
    ) -> None:
        self._conversations = conversations
        self._messages = messages

    async def open_conversation(
        self,
        *,
        tenant_id: str,
        title: str,
        member_ids: list[str],
        correlation_id: str,
        e2ee_enabled: bool = False,
        issue_livekit_token: bool = False,
    ) -> Result[dict]:
        try:
            conversation = Conversation.open(
                tenant_id=tenant_id,
                title=title,
                member_ids=member_ids,
                e2ee_enabled=e2ee_enabled,
            )
        except ValueError as exc:
            return Result.fail(str(exc))

        livekit_token = None
        if issue_livekit_token:
            from shared.connectors.registry import get_connector_adapter

            room_name = f"tenant-{tenant_id}-conv-{conversation.id}"
            adapter = get_connector_adapter("livekit")
            if adapter:
                token_result = await adapter.execute(
                    operation="create_room_token",
                    payload={"room_name": room_name, "identity": member_ids[0]},
                    config={"environment": "sandbox"},
                    idempotency_key=f"livekit:{conversation.id}",
                )
                if token_result.succeeded:
                    conversation.attach_livekit_room(room_name)
                    livekit_token = token_result.unwrap().get("result", {}).get("token")

        await self._conversations.save(conversation)
        await publish_integration_event(
            ConversationOpenedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                conversation_id=conversation.id,
                title=conversation.title,
                e2ee_enabled=conversation.e2ee_enabled,
            )
        )
        data = conversation.to_dict()
        if livekit_token:
            data["livekit_token"] = livekit_token
        return Result.ok(data)

    async def send_message(
        self,
        *,
        tenant_id: str,
        conversation_id: str,
        sender_id: str,
        body: str,
        correlation_id: str,
    ) -> Result[dict]:
        conversation = await self._conversations.find_by_id(
            tenant_id, UniqueId.from_string(conversation_id)
        )
        if not conversation:
            return Result.fail("messenger.errors.conversation_not_found")
        try:
            conversation.ensure_member(sender_id)
            message = Message.send(
                tenant_id=tenant_id,
                conversation_id=conversation.id,
                sender_id=sender_id,
                body=body,
                e2ee_enabled=conversation.e2ee_enabled,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._messages.save(message)
        await publish_integration_event(
            MessageSentIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                conversation_id=conversation.id,
                message_id=message.id,
                sender_id=sender_id,
            )
        )
        return Result.ok(message.to_dict())

    async def list_messages(
        self, tenant_id: str, conversation_id: str, *, limit: int = 50
    ) -> Result[list[dict]]:
        conversation = await self._conversations.find_by_id(
            tenant_id, UniqueId.from_string(conversation_id)
        )
        if not conversation:
            return Result.fail("messenger.errors.conversation_not_found")
        rows = await self._messages.list_by_conversation(
            tenant_id, conversation.id, limit=limit
        )
        return Result.ok([m.to_dict() for m in rows])
