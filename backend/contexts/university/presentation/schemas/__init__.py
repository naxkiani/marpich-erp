"""University API schemas."""
from pydantic import BaseModel, EmailStr, Field


class EnrollStudentRequest(BaseModel):
    student_number: str = Field(min_length=3, max_length=32)
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str = Field(min_length=1, max_length=64)
    email: EmailStr
    program_code: str = Field(min_length=2, max_length=32)
    identity_user_id: str | None = None
    document_id: str | None = None
    delivery_model: str = Field(default="degree", max_length=32)
    cohort_ref: str | None = Field(default=None, max_length=64)


class OfferCourseRequest(BaseModel):
    course_code: str = Field(min_length=2, max_length=32)
    title: str = Field(min_length=2, max_length=128)
    credits: int = Field(ge=1, le=12)
    term: str = Field(min_length=2, max_length=16)


class PostGradeRequest(BaseModel):
    student_id: str
    course_id: str
    letter_grade: str = Field(min_length=1, max_length=3)
