"""P198-B federation protocol engine and gateway unit tests."""
import base64
import hashlib

import pytest

from contexts.identity_federation.container import get_identity_federation_service, reset_identity_federation_service
from contexts.identity_federation.domain.services import protocol_engine
from contexts.identity_federation.infrastructure.protocols.oauth2_server import OAuth2AuthorizationServer


@pytest.fixture(autouse=True)
def _reset_federation():
    reset_identity_federation_service()
    yield
    reset_identity_federation_service()


@pytest.mark.unit
def test_protocol_negotiation_defaults_to_oidc():
    result = protocol_engine.negotiate_protocol(requested=None)
    assert result["negotiated_protocol"] == "oidc"
    assert result["method"] == "default"


@pytest.mark.unit
def test_protocol_catalog_includes_adapters():
    catalog = protocol_engine.build_protocol_catalog()
    assert "oauth2" in catalog["protocols"]
    assert len(catalog["adapters"]) >= 6


@pytest.mark.unit
def test_oauth2_pkce_authorization_code_flow():
    oauth = OAuth2AuthorizationServer()
    client = oauth.register_client(
        tenant_id="tenant-a",
        client_name="Test App",
        redirect_uris=["https://app.example/callback"],
    )
    verifier = "test-verifier-12345"
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    auth = oauth.authorize(
        tenant_id="tenant-a",
        client_id=client["client_id"],
        redirect_uri="https://app.example/callback",
        scope="openid profile",
        state="xyz",
        code_challenge=challenge,
        user_id="user-1",
    )
    assert "authorization_code" in auth
    tokens = oauth.token(
        tenant_id="tenant-a",
        grant_type="authorization_code",
        client_id=client["client_id"],
        code=auth["authorization_code"],
        redirect_uri="https://app.example/callback",
        code_verifier=verifier,
    )
    assert "access_token" in tokens
    intro = oauth.introspect(token=tokens["access_token"])
    assert intro["active"] is True
    oauth.revoke(token=tokens["access_token"])
    intro2 = oauth.introspect(token=tokens["access_token"])
    assert intro2["active"] is False


@pytest.mark.unit
@pytest.mark.asyncio
async def test_federation_token_client_credentials():
    svc = get_identity_federation_service()
    reg = await svc.register_oauth_client(
        "tenant-token",
        client_name="Service",
        redirect_uris=["https://svc/cb"],
        grant_types=["client_credentials"],
    )
    client = reg.unwrap()
    token = await svc.federation_token(
        "tenant-token",
        grant_type="client_credentials",
        client_id=client["client_id"],
        client_secret=client["client_secret"],
        scope="openid",
    )
    assert token.succeeded
    assert "access_token" in token.unwrap()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_scim_provision_user():
    svc = get_identity_federation_service()
    await svc.seed("tenant-scim")
    result = await svc.federation_provision(
        "tenant-scim",
        resource_type="User",
        operation="create",
        payload={"userName": "scim-user", "emails": [{"value": "scim@enterprise.dev"}]},
    )
    assert result.succeeded
    assert result.unwrap()["userName"] == "scim-user"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_oidc_discovery_and_jwks():
    svc = get_identity_federation_service()
    await svc.seed("tenant-oidc")
    discovery = (await svc.oidc_discovery("tenant-oidc")).unwrap()
    assert discovery["issuer"].endswith("/tenants/tenant-oidc/federation")
    jwks = (await svc.oidc_jwks("tenant-oidc")).unwrap()
    assert "keys" in jwks
