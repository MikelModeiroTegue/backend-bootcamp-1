from datetime import datetime, date

from sqlmodel import SQLModel, Field


class Base(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)


class Student(Base, table=True):
    first_name: str
    last_name: str
    email: str
    date_of_birth: date
