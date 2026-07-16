"""Authentication — unit tests."""
import pytest

from contexts.authentication.domain.aggregates.authentication_platform import AuthenticationCapability
from contexts.authentication.domain.services import authentication_engine as engine


@pytest.mark.unit
def test_capability_catalog_has_ten_capabilities():
    caps = {c["capability"] for c in engine.list_capability_catalog()}
    assert AuthenticationCapability.WEBAUTHN_REGISTRATION.value in caps
    assert AuthenticationCapability.OIDC_CALLBACK.value in caps
    assert len(caps) == 10


@pytest.mark.unit
def test_auth_methods_include_password_webauthn_oidc():
    methods = {m["method"] for m in engine.list_auth_methods()}
    assert methods == {"password", "webauthn", "oidc"}


@pytest.mark.unit
def test_build_oidc_authorize_url():
    url = engine.build_oidc_authorize_url(
        issuer_url="https://idp.example.com",
        client_id="marpich-portal",
        redirect_uri="http://localhost:3001/login/oidc",
        scopes="openid profile email",
        state="state-123",
        nonce="nonce-456",
    )
    assert url.startswith("https://idp.example.com/authorize?")
    assert "client_id=marpich-portal" in url
    assert "state=state-123" in url
