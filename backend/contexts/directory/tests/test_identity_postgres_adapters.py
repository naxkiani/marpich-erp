"""Directory / Authentication / Identity Risk / IGA Postgres wiring (no live DB)."""
from __future__ import annotations

from types import SimpleNamespace
from uuid import UUID

import pytest

from contexts.authentication.container import get_authentication_service, reset_authentication_service
from contexts.authentication.domain.aggregates.authentication_platform import (
    AuthenticationProfile,
    WebAuthnCredential,
)
from contexts.authentication.infrastructure.persistence.authentication_memory_store import (
    InMemoryAuthenticationProfileRepository,
)
from contexts.authentication.infrastructure.persistence.authentication_postgres_store import (
    PostgresAuthenticationProfileRepository,
    PostgresWebAuthnCredentialRepository,
    _credential_from_row,
    _profile_from_row as _auth_profile_from_row,
)
from contexts.directory.container import get_directory_service, reset_directory_service
from contexts.directory.domain.aggregates.directory_platform import DirectoryProfile, SamlProvider
from contexts.directory.infrastructure.persistence.directory_memory_store import (
    InMemoryDirectoryProfileRepository,
    InMemorySamlProviderRepository,
)
from contexts.directory.infrastructure.persistence.directory_postgres_store import (
    PostgresDirectoryProfileRepository,
    PostgresSamlProviderRepository,
    _profile_from_row as _dir_profile_from_row,
    _saml_from_row,
)
from contexts.identity_governance.container import (
    get_identity_governance_service,
    reset_identity_governance_service,
)
from contexts.identity_governance.domain.aggregates.identity_governance_platform import (
    IdentityGovernanceProfile,
)
from contexts.identity_governance.infrastructure.persistence.identity_governance_memory_store import (
    InMemoryIdentityGovernanceProfileRepository,
)
from contexts.identity_governance.infrastructure.persistence.identity_governance_postgres_store import (
    PostgresIdentityGovernanceProfileRepository,
    _profile_from_row as _iga_profile_from_row,
)
from contexts.identity_risk.container import get_identity_risk_service, reset_identity_risk_service
from contexts.identity_risk.domain.aggregates.identity_risk_platform import RiskProfile, RiskScore
from contexts.identity_risk.infrastructure.persistence.identity_risk_memory_store import (
    InMemoryRiskProfileRepository,
)
from contexts.identity_risk.infrastructure.persistence.identity_risk_postgres_store import (
    PostgresRiskProfileRepository,
    PostgresRiskScoreRepository,
    _profile_from_row as _risk_profile_from_row,
    _score_from_row,
)


@pytest.fixture(autouse=True)
def _reset(monkeypatch):
    monkeypatch.setattr("contexts.directory.container.use_postgres", lambda: False)
    monkeypatch.setattr("contexts.authentication.container.use_postgres", lambda: False)
    monkeypatch.setattr("contexts.identity_risk.container.use_postgres", lambda: False)
    monkeypatch.setattr("contexts.identity_governance.container.use_postgres", lambda: False)
    reset_directory_service()
    reset_authentication_service()
    reset_identity_risk_service()
    reset_identity_governance_service()
    yield
    reset_directory_service()
    reset_authentication_service()
    reset_identity_risk_service()
    reset_identity_governance_service()


def test_directory_container_defaults_to_memory():
    svc = get_directory_service()
    assert isinstance(svc._profiles, InMemoryDirectoryProfileRepository)
    assert isinstance(svc._saml_providers, InMemorySamlProviderRepository)


def test_directory_container_wires_postgres(monkeypatch):
    monkeypatch.setattr("contexts.directory.container.use_postgres", lambda: True)
    reset_directory_service()
    svc = get_directory_service()
    assert isinstance(svc._profiles, PostgresDirectoryProfileRepository)
    assert isinstance(svc._saml_providers, PostgresSamlProviderRepository)


def test_directory_row_mappers():
    profile = DirectoryProfile.create(tenant_id="t1", profile_ref="dir-profile-t1-0001")
    assert _dir_profile_from_row(
        SimpleNamespace(
            id=UUID(str(profile.id)),
            tenant_id=profile.tenant_id,
            profile_ref=profile.profile_ref,
            saml_enabled=True,
            ldap_enabled=True,
            scim_enabled=True,
            auto_provision=True,
            created_at=profile.created_at,
        )
    ).saml_enabled is True
    provider = SamlProvider.register(
        tenant_id="t1",
        provider_ref="saml-t1-0001",
        name="Corp",
        entity_id="https://idp.example",
        sso_url="https://idp.example/sso",
        x509_cert="CERT",
    )
    assert _saml_from_row(
        SimpleNamespace(
            id=UUID(str(provider.id)),
            tenant_id=provider.tenant_id,
            provider_ref=provider.provider_ref,
            name=provider.name,
            entity_id=provider.entity_id,
            sso_url=provider.sso_url,
            x509_cert=provider.x509_cert,
            enabled=True,
            created_at=provider.created_at,
        )
    ).entity_id == "https://idp.example"


def test_authentication_container_wires_postgres(monkeypatch):
    svc = get_authentication_service()
    assert isinstance(svc._profiles, InMemoryAuthenticationProfileRepository)
    monkeypatch.setattr("contexts.authentication.container.use_postgres", lambda: True)
    reset_authentication_service()
    svc = get_authentication_service()
    assert isinstance(svc._profiles, PostgresAuthenticationProfileRepository)
    assert isinstance(svc._credentials, PostgresWebAuthnCredentialRepository)


def test_authentication_row_mappers():
    profile = AuthenticationProfile.create(tenant_id="t1", profile_ref="auth-profile-t1-0001")
    assert _auth_profile_from_row(
        SimpleNamespace(
            id=UUID(str(profile.id)),
            tenant_id=profile.tenant_id,
            profile_ref=profile.profile_ref,
            webauthn_enabled=True,
            passkeys_required=False,
            oidc_enabled=True,
            password_enabled=True,
            created_at=profile.created_at,
        )
    ).webauthn_enabled is True
    cred = WebAuthnCredential.register(
        tenant_id="t1",
        user_id="user-1",
        credential_ref="passkey-t1-0001",
        credential_id="cred-abc",
        public_key="pk",
        sign_count=1,
        nickname="laptop",
    )
    assert _credential_from_row(
        SimpleNamespace(
            id=UUID(str(cred.id)),
            tenant_id=cred.tenant_id,
            user_id=cred.user_id,
            credential_ref=cred.credential_ref,
            credential_id=cred.credential_id,
            public_key=cred.public_key,
            sign_count=cred.sign_count,
            nickname=cred.nickname,
            transports=[],
            aaguid=None,
            created_at=cred.created_at,
            last_used_at=None,
        )
    ).credential_id == "cred-abc"


def test_identity_risk_container_wires_postgres(monkeypatch):
    svc = get_identity_risk_service()
    assert isinstance(svc._profiles, InMemoryRiskProfileRepository)
    monkeypatch.setattr("contexts.identity_risk.container.use_postgres", lambda: True)
    reset_identity_risk_service()
    svc = get_identity_risk_service()
    assert isinstance(svc._profiles, PostgresRiskProfileRepository)
    assert isinstance(svc._scores, PostgresRiskScoreRepository)


def test_identity_risk_row_mappers():
    profile = RiskProfile.create(tenant_id="t1", profile_ref="risk-profile-t1-0001")
    assert _risk_profile_from_row(
        SimpleNamespace(
            id=UUID(str(profile.id)),
            tenant_id=profile.tenant_id,
            profile_ref=profile.profile_ref,
            scoring_enabled=True,
            score_threshold=50,
            step_up_threshold=75,
            bulk_create_threshold=10,
            created_at=profile.created_at,
        )
    ).score_threshold == 50
    score = RiskScore.compute(
        tenant_id="t1",
        score_ref="score-t1-0001",
        signal_ref="signal-t1-0001",
        score=40,
        risk_level="low",
        explanation="ok",
        factors=[],
        step_up_recommended=False,
        user_id="u1",
    )
    assert _score_from_row(
        SimpleNamespace(
            id=UUID(str(score.id)),
            tenant_id=score.tenant_id,
            score_ref=score.score_ref,
            signal_ref=score.signal_ref,
            score=score.score,
            risk_level=score.risk_level,
            explanation=score.explanation,
            factors=[],
            step_up_recommended=False,
            user_id="u1",
            created_at=score.created_at,
        )
    ).risk_level == "low"


def test_identity_governance_container_wires_postgres(monkeypatch):
    svc = get_identity_governance_service()
    assert isinstance(svc._profiles, InMemoryIdentityGovernanceProfileRepository)
    monkeypatch.setattr("contexts.identity_governance.container.use_postgres", lambda: True)
    reset_identity_governance_service()
    svc = get_identity_governance_service()
    assert isinstance(svc._profiles, PostgresIdentityGovernanceProfileRepository)


def test_identity_governance_row_mapper():
    profile = IdentityGovernanceProfile.create(tenant_id="t1", profile_ref="ERP-IGP-PRF-T1-00001")
    mapped = _iga_profile_from_row(
        SimpleNamespace(
            id=UUID(str(profile.id)),
            tenant_id=profile.tenant_id,
            profile_ref=profile.profile_ref,
            access_review_frequency_days=90,
            certification_required=True,
            sod_enforcement=True,
            temporary_access_max_hours=72,
            emergency_access_max_hours=4,
            metadata_json={},
            created_at=profile.created_at,
        )
    )
    assert mapped.sod_enforcement is True
