"""WebAuthn ceremony helpers."""
from __future__ import annotations

import base64
import json
import uuid
from typing import Any

from webauthn import (
    generate_authentication_options,
    generate_registration_options,
    options_to_json,
    verify_authentication_response,
    verify_registration_response,
)
from webauthn.helpers import bytes_to_base64url, base64url_to_bytes
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialDescriptor,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

from shared.infrastructure.settings import settings


class WebAuthnService:
    def __init__(self) -> None:
        self._rp_id = settings.webauthn_rp_id
        self._rp_name = settings.webauthn_rp_name
        self._origin = settings.webauthn_origin

    def create_registration_options(
        self,
        *,
        user_id: str,
        user_email: str,
        user_display_name: str,
        existing_credentials: list[dict],
    ) -> tuple[str, dict]:
        challenge_id = str(uuid.uuid4())
        exclude = [
            PublicKeyCredentialDescriptor(id=base64url_to_bytes(c["credential_id"]))
            for c in existing_credentials
        ]
        options = generate_registration_options(
            rp_id=self._rp_id,
            rp_name=self._rp_name,
            user_id=user_id.encode("utf-8"),
            user_name=user_email,
            user_display_name=user_display_name or user_email,
            exclude_credentials=exclude,
            authenticator_selection=AuthenticatorSelectionCriteria(
                resident_key=ResidentKeyRequirement.PREFERRED,
                user_verification=UserVerificationRequirement.PREFERRED,
            ),
        )
        payload = json.loads(options_to_json(options))
        return challenge_id, payload

    def verify_registration(
        self,
        *,
        challenge_b64: str,
        credential: dict,
        expected_user_id: str,
    ) -> dict:
        verification = verify_registration_response(
            credential=credential,
            expected_challenge=base64url_to_bytes(challenge_b64),
            expected_rp_id=self._rp_id,
            expected_origin=self._origin,
            require_user_verification=False,
        )
        if verification.credential_id is None or verification.credential_public_key is None:
            raise ValueError("authentication.errors.invalid_webauthn_registration")
        return {
            "credential_id": bytes_to_base64url(verification.credential_id),
            "public_key": base64.b64encode(verification.credential_public_key).decode("ascii"),
            "sign_count": verification.sign_count,
            "aaguid": str(verification.aaguid) if verification.aaguid else None,
            "user_id": expected_user_id,
        }

    def create_authentication_options(
        self,
        *,
        credentials: list[dict],
    ) -> tuple[str, dict]:
        if not credentials:
            raise ValueError("authentication.errors.no_passkeys")
        challenge_id = str(uuid.uuid4())
        allow = [
            PublicKeyCredentialDescriptor(id=base64url_to_bytes(c["credential_id"]))
            for c in credentials
        ]
        options = generate_authentication_options(
            rp_id=self._rp_id,
            allow_credentials=allow,
            user_verification=UserVerificationRequirement.PREFERRED,
        )
        payload = json.loads(options_to_json(options))
        return challenge_id, payload

    def verify_authentication(
        self,
        *,
        challenge_b64: str,
        credential: dict,
        stored_credential: dict,
    ) -> dict:
        verification = verify_authentication_response(
            credential=credential,
            expected_challenge=base64url_to_bytes(challenge_b64),
            expected_rp_id=self._rp_id,
            expected_origin=self._origin,
            credential_public_key=base64.b64decode(stored_credential["public_key"]),
            credential_current_sign_count=stored_credential["sign_count"],
            require_user_verification=False,
        )
        return {
            "credential_id": stored_credential["credential_id"],
            "sign_count": verification.new_sign_count,
            "user_id": stored_credential["user_id"],
        }

    @staticmethod
    def challenge_from_options(options: dict[str, Any]) -> str:
        return str(options["challenge"])
