"""SCIM provisioning helpers."""
from __future__ import annotations

from contexts.directory.domain.services import directory_engine as engine


class ScimProvisioningService:
    def build_user_response(
        self,
        *,
        user_id: str,
        email: str,
        display_name: str,
        external_id: str,
    ) -> dict:
        return engine.build_scim_user_resource(
            user_id=user_id,
            email=email,
            display_name=display_name,
            external_id=external_id,
        )

    def parse_create_user(self, payload: dict) -> tuple[str, str, str]:
        email = ""
        for item in payload.get("emails", []):
            if item.get("primary") and item.get("value"):
                email = str(item["value"]).strip().lower()
                break
        if not email:
            username = payload.get("userName")
            if isinstance(username, str) and "@" in username:
                email = username.strip().lower()
        display_name = str(payload.get("displayName") or email.split("@")[0] or "SCIM User")
        external_id = str(payload.get("externalId") or email)
        if not email:
            raise ValueError("directory.errors.scim_email_required")
        return email, display_name, external_id
