"""Domain specifications — tactical DDD (P200-B4)."""
from __future__ import annotations

from contexts.identity_federation.domain.aggregates.federation_platform import (
    IdentityLink,
    IdentityProvider,
    TrustRelationship,
)
from contexts.identity_federation.domain.strategic.ubiquitous_language import TrustStatus


class ActiveTrustSpec:
    def is_satisfied_by(self, trust: TrustRelationship) -> bool:
        return trust.status == TrustStatus.ACTIVE.value and 0 <= trust.trust_score <= 100


class EnabledProviderSpec:
    def is_satisfied_by(self, provider: IdentityProvider) -> bool:
        return bool(provider.enabled and provider.protocol and provider.provider_ref)


class LinkableSubjectSpec:
    def is_satisfied_by(self, link: IdentityLink) -> bool:
        return bool(
            link.tenant_id
            and link.user_id
            and link.provider_id
            and link.external_subject
            and link.link_status != "unlinked"
        )
