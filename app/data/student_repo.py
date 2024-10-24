from abc import ABC, abstractmethod
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlmodel import Session, select

from app.data.models import Grade, Student
from app.data.schemas import CreateUserSchema, UpdateUserSchema
from app.domain.exceptions import StudentNotFound


class AbstractRepo(ABC):

    @abstractmethod
    def create_student(self, data: CreateUserSchema): ...

    @abstractmethod
    def get_student_by_id(self, student_id: int): ...

    @abstractmethod
    def get_all_students(self): ...

    @abstractmethod
    def update_student(self, student_id: int, data: UpdateUserSchema): ...

    @abstractmethod
    def delete_student(self, student_id: int): ...
    
    @abstractmethod
    def get_my_grades(self, student_id: int): ...

class StudentRepo(AbstractRepo):
    def __init__(self, session: Session):
        self._session = session

    def create_student(self, data: CreateUserSchema) -> Student:
        student = Student(**dict(data))
        if student.userRole == "Student":
            self._session.add(student)
            self._session.commit()
            self._session.refresh(student)
        
        return student
    
    def get_student_by_id(self, student_id: int) -> Student | None:
        return self._session.exec(select(Student).where(Student.id == student_id)).one_or_none()

    def get_all_students(self) -> Sequence[Student]:
        return self._session.exec(select(Student)).all()

    def update_student(self, student_id: int, data: UpdateUserSchema):
        student = self.get_student_by_id(student_id)
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

    def delete_student(self, student_id: int) -> bool:
        student = self._session.exec(select(Student).where(Student.id == student_id)).one_or_none()
        if not student:
            return False
        self._session.delete(student)
        self._session.commit()
        return True
    
    def get_my_grades(self, student_id: int) -> Grade:
        my_grades = self._session.exec(select(Grade).where(Grade.student_id == student_id)).one_or_none()
        if not my_grades:
            raise HTTPException (
                status_code= status.HTTP_204_NO_CONTENT, 
                details = "No Content was Found",
                headers = {"WWW-Authenticate":"Bearer"}
            )
        return my_grades


