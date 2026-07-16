"""Identity lifecycle — unit tests."""
import pytest

from contexts.identity_lifecycle.domain.aggregates.identity_lifecycle_platform import (
    LifecycleAction,
    LifecycleCapability,
)
from contexts.identity_lifecycle.domain.services import identity_lifecycle_engine as engine
from contexts.identity_lifecycle.domain.services import lifecycle_workflow_engine as workflow


@pytest.mark.unit
def test_capability_catalog_has_fourteen_capabilities():
    caps = {c["capability"] for c in engine.list_capability_catalog()}
    assert LifecycleCapability.LIFECYCLE_WORKFLOW_ENGINE.value in caps
    assert LifecycleCapability.AI_LIFECYCLE_ASSISTANT.value in caps
    assert len(caps) == 14


@pytest.mark.unit
def test_workflow_supports_registration_to_activation():
    assert workflow.can_transition("registered", LifecycleAction.EMAIL_VERIFICATION.value)
    assert workflow.can_transition("verified", LifecycleAction.ACCOUNT_ACTIVATION.value)
    assert workflow.resolve_transition("active", LifecycleAction.SUSPENSION.value) == "suspended"


@pytest.mark.unit
def test_workflow_supports_merge_archive_delete():
    assert workflow.can_transition("active", LifecycleAction.MERGE_IDENTITIES.value)
    assert workflow.can_transition("active", LifecycleAction.IDENTITY_ARCHIVE.value)
    assert workflow.can_transition("soft_deleted", LifecycleAction.HARD_DELETE.value)
