"""Directory — unit tests."""
import base64

import pytest

from contexts.directory.domain.aggregates.directory_platform import DirectoryCapability
from contexts.directory.domain.services import directory_engine as engine


@pytest.mark.unit
def test_capability_catalog_has_ten_capabilities():
    caps = {c["capability"] for c in engine.list_capability_catalog()}
    assert DirectoryCapability.SAML_PROVIDER_REGISTRY.value in caps
    assert DirectoryCapability.SCIM_USER_PROVISIONING.value in caps
    assert len(caps) == 10


@pytest.mark.unit
def test_directory_sources_include_saml_ldap_scim():
    sources = {s["source"] for s in engine.list_directory_sources()}
    assert sources == {"saml", "ldap", "scim"}


@pytest.mark.unit
def test_build_saml_authn_request():
    url = engine.build_saml_authn_request(
        sp_entity_id="urn:marpich:sp",
        acs_url="http://localhost:3001/login/saml/acs",
        idp_sso_url="https://idp.enterprise.dev/sso",
        request_id="_test123",
    )
    assert url.startswith("https://idp.enterprise.dev/sso?")
    assert "SAMLRequest=" in url


@pytest.mark.unit
def test_extract_email_from_saml_response():
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<samlp:Response xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">'
        '<saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">'
        "<saml:Subject><saml:NameID>saml-user@enterprise.dev</saml:NameID></saml:Subject>"
        "</saml:Assertion></samlp:Response>"
    )
    encoded = base64.b64encode(xml.encode("utf-8")).decode("ascii")
    assert engine.extract_email_from_saml_response(encoded) == "saml-user@enterprise.dev"
