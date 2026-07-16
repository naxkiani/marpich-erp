"""Directory API schemas."""
from __future__ import annotations

from pydantic import BaseModel


class RegisterSamlProviderRequest(BaseModel):
    name: str
    entity_id: str
    sso_url: str
    x509_cert: str


class SamlAuthorizeRequest(BaseModel):
    provider_ref: str


class SamlAcsRequest(BaseModel):
    SAMLResponse: str
    RelayState: str


class RegisterLdapConnectorRequest(BaseModel):
    name: str
    host: str
    port: int = 389
    bind_dn: str
    bind_password: str
    base_dn: str
    user_filter: str = "(objectClass=person)"


class LdapSyncRequest(BaseModel):
    connector_ref: str


class RegisterScimProviderRequest(BaseModel):
    name: str
    bearer_token: str | None = None


class ScimCreateUserRequest(BaseModel):
    schemas: list[str] = ["urn:ietf:params:scim:schemas:core:2.0:User"]
    userName: str | None = None
    displayName: str | None = None
    externalId: str | None = None
    active: bool = True
    emails: list[dict] = []
