from sqlmodel import SQLModel, Field
from datetime import date, datetime


class User_BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    id: int | None = Field(default=None, primary_key=True)
    userName: str = Field(index=True, nullable=False, unique=True)
    firstName: str = Field(nullable=False)
    lastName: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True, description="Must be a unique email")
    dateOfBirth: date
    hashed_password: str


class Student(User_BaseModel, table=True):
    userRole: str = "Student"


class Grade(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(nullable=False, foreign_key="Student.id")
    pure_maths: int = Field(nullable=False, ge=0, le=20)
    chemistry: int = Field(nullable=False, ge=0, le=20)
    biology: int = Field(nullable=False, ge=0, le=20)
    computer_science: int = Field(nullable=False, ge=0, le=20)
    physics: int = Field(nullable=False, ge=0, le=20)


class Instructor(User_BaseModel, table=True):
    userRole: str = "Instructor"
