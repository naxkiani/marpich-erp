"""SCIM 2.0 provisioning server."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

_users: dict[str, dict] = {}
_groups: dict[str, dict] = {}


class ScimServer:
    SCHEMA_USER = "urn:ietf:params:scim:schemas:core:2.0:User"
    SCHEMA_GROUP = "urn:ietf:params:scim:schemas:core:2.0:Group"

    def create_user(self, *, tenant_id: str, payload: dict) -> dict:
        user_id = str(uuid.uuid4())
        user = {
            "schemas": [self.SCHEMA_USER],
            "id": user_id,
            "externalId": payload.get("externalId"),
            "userName": payload.get("userName"),
            "name": payload.get("name", {}),
            "emails": payload.get("emails", []),
            "active": payload.get("active", True),
            "meta": {
                "resourceType": "User",
                "created": datetime.now(UTC).isoformat(),
                "location": f"/scim/v2/Users/{user_id}",
            },
        }
        _users[f"{tenant_id}:{user_id}"] = user
        return user

    def get_user(self, *, tenant_id: str, user_id: str) -> dict | None:
        return _users.get(f"{tenant_id}:{user_id}")

    def patch_user(self, *, tenant_id: str, user_id: str, operations: list[dict]) -> dict | None:
        user = _users.get(f"{tenant_id}:{user_id}")
        if not user:
            return None
        for op in operations:
            path = op.get("path", "")
            if op.get("op") == "replace":
                if path == "active":
                    user["active"] = op.get("value")
                elif path.startswith("emails"):
                    user["emails"] = op.get("value", user.get("emails"))
        return user

    def delete_user(self, *, tenant_id: str, user_id: str) -> bool:
        key = f"{tenant_id}:{user_id}"
        if key in _users:
            del _users[key]
            return True
        return False

    def create_group(self, *, tenant_id: str, payload: dict) -> dict:
        group_id = str(uuid.uuid4())
        group = {
            "schemas": [self.SCHEMA_GROUP],
            "id": group_id,
            "displayName": payload.get("displayName"),
            "members": payload.get("members", []),
            "meta": {"resourceType": "Group", "created": datetime.now(UTC).isoformat()},
        }
        _groups[f"{tenant_id}:{group_id}"] = group
        return group

    def bulk(self, *, tenant_id: str, operations: list[dict]) -> dict:
        results = []
        for op in operations:
            method = op.get("method", "POST").upper()
            if method == "POST" and op.get("path") == "/Users":
                results.append({"status": "201", "response": self.create_user(tenant_id=tenant_id, payload=op.get("data", {}))})
            elif method == "DELETE":
                uid = op.get("path", "").split("/")[-1]
                ok = self.delete_user(tenant_id=tenant_id, user_id=uid)
                results.append({"status": "204" if ok else "404"})
        return {"schemas": ["urn:ietf:params:scim:api:messages:2.0:BulkResponse"], "Operations": results}

    @classmethod
    def reset(cls) -> None:
        _users.clear()
        _groups.clear()
