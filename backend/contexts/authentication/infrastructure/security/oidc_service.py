"""OIDC federation helpers."""
from __future__ import annotations

import httpx

from contexts.authentication.domain.services import authentication_engine as engine


class OidcFederationService:
    async def exchange_code(
        self,
        *,
        issuer_url: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        code: str,
    ) -> dict:
        token_url = f"{issuer_url.rstrip('/')}/token"
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                token_url,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "client_id": client_id,
                    "client_secret": client_secret,
                },
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json()

    def build_authorize_url(
        self,
        *,
        issuer_url: str,
        client_id: str,
        redirect_uri: str,
        scopes: str,
        state: str,
        nonce: str,
    ) -> str:
        return engine.build_oidc_authorize_url(
            issuer_url=issuer_url,
            client_id=client_id,
            redirect_uri=redirect_uri,
            scopes=scopes,
            state=state,
            nonce=nonce,
        )

    @staticmethod
    def extract_email_from_id_token(id_token_payload: dict) -> str | None:
        email = id_token_payload.get("email")
        if isinstance(email, str) and email:
            return email
        preferred = id_token_payload.get("preferred_username")
        if isinstance(preferred, str) and "@" in preferred:
            return preferred
        return None
