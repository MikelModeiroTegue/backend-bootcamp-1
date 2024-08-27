from typing import Generator

from sqlmodel import create_engine, SQLModel, Session

engine = create_engine(url="sqlite:///students.db")

def create_tables():
    SQLModel.metadata.create_all(engine)



def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
