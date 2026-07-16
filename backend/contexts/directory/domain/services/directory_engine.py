"""Directory engine — catalog, policy keys, SAML/LDAP helpers."""
from __future__ import annotations

import base64
import secrets
import uuid
import zlib
from datetime import UTC, datetime
from urllib.parse import quote_plus, urlencode
from xml.etree import ElementTree as ET

from contexts.directory.domain.aggregates.directory_platform import DirectoryCapability

POLICY_KEYS = [
    "directory.saml.enabled",
    "directory.ldap.enabled",
    "directory.scim.enabled",
    "directory.sync.auto_provision",
]

CAPABILITY_LABELS = {
    DirectoryCapability.SAML_PROVIDER_REGISTRY.value: "SAML Provider Registry",
    DirectoryCapability.SAML_AUTHORIZATION.value: "SAML Authorization",
    DirectoryCapability.SAML_ASSERTION_CONSUMER.value: "SAML Assertion Consumer",
    DirectoryCapability.LDAP_CONNECTOR_REGISTRY.value: "LDAP Connector Registry",
    DirectoryCapability.LDAP_DIRECTORY_SYNC.value: "LDAP Directory Sync",
    DirectoryCapability.SCIM_PROVIDER_REGISTRY.value: "SCIM Provider Registry",
    DirectoryCapability.SCIM_USER_PROVISIONING.value: "SCIM User Provisioning",
    DirectoryCapability.DIRECTORY_SYNC_WORKER.value: "Directory Sync Worker",
    DirectoryCapability.POLICY_DRIVEN_DIRECTORY.value: "Policy-Driven Directory",
    DirectoryCapability.DIRECTORY_API.value: "Directory API",
}

DIRECTORY_SOURCES = [
    {"source": "saml", "label": "SAML Federation", "sync_mode": "login"},
    {"source": "ldap", "label": "LDAP / Active Directory", "sync_mode": "batch"},
    {"source": "scim", "label": "SCIM Provisioning", "sync_mode": "push"},
]

SAML_NS = {
    "samlp": "urn:oasis:names:tc:SAML:2.0:protocol",
    "saml": "urn:oasis:names:tc:SAML:2.0:assertion",
}


def list_capability_catalog() -> list[dict]:
    return [
        {"capability": c.value, "label": CAPABILITY_LABELS.get(c.value, c.name.replace("_", " ").title())}
        for c in DirectoryCapability
    ]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def list_directory_sources() -> list[dict]:
    return list(DIRECTORY_SOURCES)


def dependency_map() -> dict:
    return {
        "nodes": [
            {"id": "directory", "type": "platform", "label": "Directory Platform"},
            {"id": "identity", "type": "platform", "label": "Identity Core"},
            {"id": "authentication", "type": "platform", "label": "Authentication"},
        ],
        "edges": [
            {"from": "directory", "to": "identity", "type": "user_provision"},
            {"from": "authentication", "to": "directory", "type": "federation_delegate"},
        ],
    }


def new_saml_request_id() -> str:
    return f"_{uuid.uuid4().hex}"


def new_saml_relay_state() -> str:
    return secrets.token_urlsafe(24)


def encode_saml_redirect(value: str) -> str:
    compressed = zlib.compress(value.encode("utf-8"))[2:-4]
    return quote_plus(base64.b64encode(compressed).decode("ascii"))


def build_saml_authn_request(
    *,
    sp_entity_id: str,
    acs_url: str,
    idp_sso_url: str,
    request_id: str | None = None,
) -> str:
    request_id = request_id or new_saml_request_id()
    issue_instant = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<samlp:AuthnRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" '
        f'xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" '
        f'ID="{request_id}" Version="2.0" IssueInstant="{issue_instant}" '
        f'Destination="{idp_sso_url}" AssertionConsumerServiceURL="{acs_url}" '
        f'ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST">'
        f"<saml:Issuer>{sp_entity_id}</saml:Issuer>"
        "</samlp:AuthnRequest>"
    )
    params = {"SAMLRequest": encode_saml_redirect(xml)}
    separator = "&" if "?" in idp_sso_url else "?"
    return f"{idp_sso_url}{separator}{urlencode(params)}"


def extract_email_from_saml_response(saml_response_b64: str) -> str | None:
    try:
        raw = base64.b64decode(saml_response_b64)
        root = ET.fromstring(raw)
    except (ET.ParseError, ValueError):
        return None
    for elem in root.iter():
        if elem.tag.endswith("NameID") and elem.text:
            value = elem.text.strip()
            if "@" in value:
                return value.lower()
    for elem in root.iter():
        if elem.tag.endswith("Attribute") and elem.get("Name") in {"email", "mail", "emailAddress"}:
            for child in elem:
                if child.text and "@" in child.text:
                    return child.text.strip().lower()
    return None


def build_scim_user_resource(
    *,
    user_id: str,
    email: str,
    display_name: str,
    external_id: str,
) -> dict:
    return {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": user_id,
        "externalId": external_id,
        "userName": email,
        "displayName": display_name,
        "active": True,
        "emails": [{"value": email, "primary": True}],
    }
