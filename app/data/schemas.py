from pydantic import BaseModel, Field
from datetime import date
from typing import Any, Optional


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class UserSchema(BaseModel):
    userName: str
    firstName: str
    lastName: str
    email: str = Field(default=None, description="Email Address and must be unique")
    dateOfBirth: date
    userRole: str
    
    class Config:
        orm_mode = True  # This enables ORM mode for compatibility


class CreateUserSchema(UserSchema):
    password: str


class UpdateUserSchema(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    dateOfBirth: Optional[date]


class GradeSchema(BaseModel):
    student_id: int
    pure_maths: int
    chemistry: int
    biology: int
    computer_science: int
    physics: int


class CreateStudentResponse(CreateUserSchema):
    id: int


class GetStudentsResponse(BaseModel):
    students: list[dict[str, Any]]


class UpdateStudentResponse(CreateStudentResponse): ...


class GetStudentResponse(CreateStudentResponse): ...


class GetInstructorsResponse(BaseModel):
    instructors: list[dict[str, Any]]


class UpdateInstructorResponse(CreateStudentResponse): ...


class GetInstructorResponse(CreateStudentResponse): ...