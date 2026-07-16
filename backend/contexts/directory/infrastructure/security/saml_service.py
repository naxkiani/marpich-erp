"""SAML federation helpers."""
from __future__ import annotations

from contexts.directory.domain.services import directory_engine as engine


class SamlFederationService:
    def build_login_redirect(
        self,
        *,
        sp_entity_id: str,
        acs_url: str,
        idp_sso_url: str,
    ) -> tuple[str, str]:
        request_id = engine.new_saml_request_id()
        relay_state = engine.new_saml_relay_state()
        url = engine.build_saml_authn_request(
            sp_entity_id=sp_entity_id,
            acs_url=acs_url,
            idp_sso_url=idp_sso_url,
            request_id=request_id,
        )
        return url, relay_state

    def extract_email(self, saml_response: str) -> str | None:
        return engine.extract_email_from_saml_response(saml_response)
