"""University DI container + LMS event subscriptions."""
from __future__ import annotations

from contexts.university.application.service import UniversityApplicationService
from contexts.university.infrastructure.acl.lms_events import handle_lms_batch_synced
from contexts.university.infrastructure.persistence.memory_store import (
    InMemoryCourseRepository,
    InMemoryGradeRepository,
    InMemoryStudentRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: UniversityApplicationService | None = None
_registered = False

_LMS_EVENTS = (
    "integration.moodle.batch.synced",
    "integration.google_classroom.batch.synced",
)


def get_university_service() -> UniversityApplicationService:
    global _service, _registered
    if _service is None:
        _service = UniversityApplicationService(
            students=InMemoryStudentRepository(),
            courses=InMemoryCourseRepository(),
            grades=InMemoryGradeRepository(),
        )
    if not _registered:
        for name in _LMS_EVENTS:
            InProcessEventBus.subscribe(name, handle_lms_batch_synced)
        _registered = True
    return _service


def reset_university_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
