"""Human Resources API schemas."""
from pydantic import BaseModel, Field


class HireEmployeeRequest(BaseModel):
    email: str = Field(min_length=3, max_length=256, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    full_name: str = Field(min_length=1, max_length=128)
    job_title: str | None = Field(default=None, max_length=128)
    department: str | None = Field(default=None, max_length=128)
    employee_number: str | None = Field(default=None, max_length=64)


class TerminateEmployeeRequest(BaseModel):
    reason: str | None = Field(default=None, max_length=512)
