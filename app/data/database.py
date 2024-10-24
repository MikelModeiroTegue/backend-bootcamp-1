from sqlmodel import create_engine, SQLModel, Session
from contextlib import contextmanager

# Database connection
DATABASE_URL = "sqlite:///school.db"
engine = create_engine(DATABASE_URL)


def create_tables():
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
