"""Messenger application service."""
from __future__ import annotations

from contexts.messenger.domain.aggregates.conversation import Conversation
from contexts.messenger.domain.aggregates.message import Message
from contexts.messenger.domain.events.integration_events import (
    ConversationOpenedIntegration,
    LiveKitTokenIssuedIntegration,
    MessageSentIntegration,
)
from contexts.messenger.domain.ports.realtime_media import IRealtimeMediaPort
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
        realtime_media: IRealtimeMediaPort,
    ) -> None:
        self._conversations = conversations
        self._messages = messages
        self._realtime = realtime_media

    async def open_conversation(
        self,
        *,
        tenant_id: str,
        title: str,
        member_ids: list[str],
        correlation_id: str,
        e2ee_enabled: bool = False,
        issue_livekit_token: bool = False,
        requester_id: str | None = None,
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

        livekit_meta: dict | None = None
        if issue_livekit_token:
            identity = requester_id or conversation.member_ids[0]
            room_name = f"tenant-{tenant_id}-conv-{conversation.id}"
            token_result = await self._realtime.create_room_token(
                room_name=room_name,
                identity=identity,
                idempotency_key=f"livekit:{conversation.id}:{identity}",
            )
            if not token_result.succeeded:
                return token_result
            livekit_meta = token_result.unwrap()
            conversation.attach_livekit_room(room_name)

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
        if livekit_meta:
            data["livekit_token"] = livekit_meta.get("token")
            data["livekit_url"] = livekit_meta.get("url")
            data["livekit_simulated"] = bool(livekit_meta.get("simulated", True))
            data["livekit_expires_at"] = livekit_meta.get("expires_at")
            await publish_integration_event(
                LiveKitTokenIssuedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id,
                    conversation_id=conversation.id,
                    room_name=conversation.livekit_room_name or "",
                    identity=str(livekit_meta.get("identity") or ""),
                    simulated=bool(livekit_meta.get("simulated", True)),
                )
            )
        return Result.ok(data)

    async def issue_livekit_token(
        self,
        *,
        tenant_id: str,
        conversation_id: str,
        requester_id: str,
        correlation_id: str,
    ) -> Result[dict]:
        conversation = await self._conversations.find_by_id(
            tenant_id, UniqueId.from_string(conversation_id)
        )
        if not conversation:
            return Result.fail("messenger.errors.conversation_not_found")
        try:
            conversation.ensure_member(requester_id)
        except ValueError as exc:
            return Result.fail(str(exc))

        room_name = conversation.livekit_room_name or (
            f"tenant-{tenant_id}-conv-{conversation.id}"
        )
        token_result = await self._realtime.create_room_token(
            room_name=room_name,
            identity=requester_id,
            idempotency_key=f"livekit:{conversation.id}:{requester_id}",
        )
        if not token_result.succeeded:
            return token_result
        meta = token_result.unwrap()
        if not conversation.livekit_room_name:
            conversation.attach_livekit_room(room_name)
            await self._conversations.save(conversation)

        await publish_integration_event(
            LiveKitTokenIssuedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                conversation_id=conversation.id,
                room_name=room_name,
                identity=requester_id,
                simulated=bool(meta.get("simulated", True)),
            )
        )
        return Result.ok(
            {
                "conversation_id": str(conversation.id),
                "room_name": room_name,
                "token": meta.get("token"),
                "url": meta.get("url"),
                "identity": requester_id,
                "expires_at": meta.get("expires_at"),
                "simulated": bool(meta.get("simulated", True)),
            }
        )

    async def send_message(
        self,
        *,
        tenant_id: str,
        conversation_id: str,
        sender_id: str,
        body: str = "",
        ciphertext: str | None = None,
        ciphertext_type: str | None = None,
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
                ciphertext=ciphertext,
                ciphertext_type=ciphertext_type,
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
