"""SAML 2.0 platform — IdP/SP metadata, SSO, SLO helpers."""
from __future__ import annotations

import base64
import uuid
from datetime import UTC, datetime
from typing import Any
from xml.sax.saxutils import escape


class SamlPlatform:
    def idp_metadata(self, *, entity_id: str, sso_url: str, slo_url: str | None = None) -> str:
        slo = f'<SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="{escape(slo_url)}"/>' if slo_url else ""
        return f"""<?xml version="1.0"?>
<EntityDescriptor xmlns="urn:oasis:names:tc:SAML:2.0:metadata" entityID="{escape(entity_id)}">
  <IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="{escape(sso_url)}"/>
    {slo}
  </IDPSSODescriptor>
</EntityDescriptor>"""

    def sp_metadata(self, *, entity_id: str, acs_url: str) -> str:
        return f"""<?xml version="1.0"?>
<EntityDescriptor xmlns="urn:oasis:names:tc:SAML:2.0:metadata" entityID="{escape(entity_id)}">
  <SPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="{escape(acs_url)}" index="0"/>
  </SPSSODescriptor>
</EntityDescriptor>"""

    def authn_request_redirect(self, *, idp_sso_url: str, sp_entity_id: str, relay_state: str = "") -> str:
        request_id = f"_{uuid.uuid4().hex}"
        issue_instant = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        xml = (
            f'<samlp:AuthnRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" '
            f'ID="{request_id}" Version="2.0" IssueInstant="{issue_instant}" '
            f'AssertionConsumerServiceURL="{escape(sp_entity_id)}" '
            f'ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST">'
            f'<saml:Issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">{escape(sp_entity_id)}</saml:Issuer>'
            f"</samlp:AuthnRequest>"
        )
        encoded = base64.b64encode(xml.encode()).decode()
        sep = "&" if "?" in idp_sso_url else "?"
        url = f"{idp_sso_url}{sep}SAMLRequest={encoded}"
        if relay_state:
            url += f"&RelayState={escape(relay_state)}"
        return url

    def parse_response_email(self, *, saml_response_b64: str) -> dict:
        try:
            decoded = base64.b64decode(saml_response_b64).decode(errors="ignore")
            email = None
            for tag in ("Email", "email", "NameID"):
                if f"<{tag}>" in decoded or f'{tag}="' in decoded:
                    start = decoded.find(tag)
                    fragment = decoded[start : start + 200]
                    if "@" in fragment:
                        for part in fragment.split("<"):
                            if "@" in part:
                                email = part.split(">")[0].split('"')[0].strip()
                                break
            return {"parsed": True, "email": email, "assertion_valid": bool(email)}
        except Exception as exc:
            return {"parsed": False, "error": str(exc), "assertion_valid": False}

    def attribute_statement(self, *, attributes: dict[str, Any]) -> dict:
        return {"attributes": [{"name": k, "value": v} for k, v in attributes.items()]}
