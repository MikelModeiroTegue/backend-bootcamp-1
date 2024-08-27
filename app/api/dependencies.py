from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.data.database import get_db
from app.data.repo import StudentRepo, AbstractRepo


def get_repo(session: Annotated[Session, Depends(get_db)]) -> AbstractRepo:
    return StudentRepo(session)