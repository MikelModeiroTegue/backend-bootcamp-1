from datetime import date
from typing import Optional, Any

from pydantic import BaseModel


class CreateStudentSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    date_of_birth: date


class UpdateStudentSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    date_of_birth: Optional[date]


class CreateStudentResponse(CreateStudentSchema):
    id: int


class GetStudentsResponse(BaseModel):
    students: list[dict[str, Any]]


class UpdateStudentResponse(CreateStudentResponse): ...


class GetStudentResponse(CreateStudentResponse): ...