"""Moodle LMS connector adapter — Integration Platform only (no domain HTTP).

Sandbox/dev returns deterministic fixture records. Production would call Moodle
Web Services via Integration secrets (api_token) — never from university domain.
"""
from __future__ import annotations

from shared.application.result import Result
from shared.connectors.stub_adapter import BaseConnectorAdapter

_OPS = ["courses_sync", "enrollments_sync", "grades_push", "test_connection"]


class MoodleAdapter(BaseConnectorAdapter):
    def __init__(self) -> None:
        super().__init__("moodle", _OPS)

    async def test_connection(self, *, config: dict, secret: str = "") -> Result[dict]:
        if not config.get("base_url"):
            return Result.fail("moodle.base_url_required")
        return Result.ok(
            {
                "connector_type": self.connector_type,
                "connected": True,
                "latency_ms": 35,
                "environment": config.get("environment", "sandbox"),
                "site": config.get("base_url"),
            }
        )

    async def execute(
        self,
        *,
        operation: str,
        payload: dict,
        config: dict,
        secret: str = "",
        idempotency_key: str = "",
    ) -> Result[dict]:
        if operation not in self._operations:
            return Result.fail(f"unsupported_operation:{operation}")
        if operation == "test_connection":
            return await self.test_connection(config=config, secret=secret)

        fixtures = config.get("fixtures") if isinstance(config.get("fixtures"), dict) else {}
        if operation == "courses_sync":
            courses = fixtures.get("courses") or [
                {
                    "lms_course_id": "mdl-CS101",
                    "course_code": "CS101",
                    "title": "Intro Computing (Moodle)",
                    "credits": 3,
                    "term": "FALL26",
                },
                {
                    "lms_course_id": "mdl-MATH201",
                    "course_code": "MATH201",
                    "title": "Discrete Math (Moodle)",
                    "credits": 4,
                    "term": "FALL26",
                },
            ]
            return Result.ok(self._wrap(operation, idempotency_key, {"courses": courses}))

        if operation == "enrollments_sync":
            enrollments = fixtures.get("enrollments") or [
                {
                    "lms_user_id": "mdl-u-1001",
                    "student_number": "S1001",
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "email": "ada@moodle.demo",
                    "program_code": "CS",
                    "lms_course_id": "mdl-CS101",
                }
            ]
            return Result.ok(self._wrap(operation, idempotency_key, {"enrollments": enrollments}))

        # grades_push — in sandbox, treat payload as push confirmation and echo grades
        grades = payload.get("grades") or fixtures.get("grades") or [
            {
                "lms_user_id": "mdl-u-1001",
                "student_number": "S1001",
                "lms_course_id": "mdl-CS101",
                "course_code": "CS101",
                "letter_grade": "A",
            }
        ]
        return Result.ok(self._wrap(operation, idempotency_key, {"grades": grades, "direction": "push"}))

    def _wrap(self, operation: str, idempotency_key: str, data: dict) -> dict:
        return {
            "connector_type": self.connector_type,
            "operation": operation,
            "status": "completed",
            "provider": "moodle",
            "idempotency_key": idempotency_key or None,
            "result": {"simulated": True, **data},
        }
