from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.data.database import get_session
from app.data.student_repo import StudentRepo, AbstractRepo


def get_repo(session: Annotated[Session, Depends(get_session)]) -> AbstractRepo:
    return StudentRepo(session)