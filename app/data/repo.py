from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import delete
from sqlmodel import Session, select

from app.data.models import Student
from app.data.schemas import CreateStudentSchema, UpdateStudentSchema
from app.domain.exceptions import StudentNotFound


class AbstractRepo(ABC):

    @abstractmethod
    def create_student(self, data: CreateStudentSchema): ...

    @abstractmethod
    def get_student_by_id(self, user_id: int): ...

    @abstractmethod
    def get_all_students(self): ...

    @abstractmethod
    def update_student(self, user_id: int, data: UpdateStudentSchema): ...

    @abstractmethod
    def delete_student(self, user_id: int): ...


class StudentRepo(AbstractRepo):
    def __init__(self, session: Session):
        self._session = session

    def create_student(self, data: CreateStudentSchema) -> Student:
        student = Student(**dict(data))
        self._session.add(student)
        self._session.commit()
        self._session.refresh(student)
        return student

    def get_student_by_id(self, user_id: int) -> Student | None:
        return self._session.exec(select(Student).where(Student.id == user_id)).one_or_none()


    def get_all_students(self) -> Sequence[Student]:
        return self._session.exec(select(Student)).all()

    def update_student(self, user_id: int, data: UpdateStudentSchema):
        student = self.get_student_by_id(user_id)
        if not student:
            return None
        student.first_name = data.first_name
        student.last_name = data.last_name
        student.email = data.email
        student.date_of_birth = data.date_of_birth

        self._session.add(student)
        self._session.commit()
        self._session.refresh(student)
        return student

    def delete_student(self, user_id: int) -> bool:
        user = self._session.exec(select(Student).where(Student.id == user_id)).one_or_none()
        if not user:
            return False
        self._session.delete(user)
        self._session.commit()
        return True


