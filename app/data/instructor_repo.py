from abc import ABC, abstractmethod
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlmodel import Session, desc, select

from app.data.models import Instructor, Student, Grade
from app.data.schemas import CreateUserSchema, GradeSchema, UpdateUserSchema
from app.domain.exceptions import StudentNotFound
from app.domain.student_service import get_my_grades


class AbstractRepo(ABC):
    @abstractmethod
    def create_instructor(self, data: CreateUserSchema): ...

    @abstractmethod
    def get_instructor_by_id(self, instructor_id: int): ...

    @abstractmethod
    def get_all_instructors(self): ...

    @abstractmethod
    def update_instructor(self, instructor_id: int, data: UpdateUserSchema): ...

    @abstractmethod
    def delete_instructor(self, instructor_id: int): ...
    
    @abstractmethod
    def get_top_students(self): ...
    
    @abstractmethod
    def add_new_grade(self, student_id: int, data: GradeSchema): ...
    
    @abstractmethod
    def update_grade(self, student_id: int, data: GradeSchema): ...
    
    @abstractmethod
    def view_grades(self): ...



class InstructorRepo(AbstractRepo):
    
    def __init__(self, session: Session):
        self._session = session


    def create_instructor(self, data: CreateUserSchema) -> Instructor:
        instructor = Instructor(**dict(data))
        if instructor.userRole == "Instructor":
            self._session.add(instructor)
            self._session.commit()
            self._session.refresh(instructor)
        
        return instructor


    def get_instructor_by_id(self, instructor_id: int) -> Instructor | None:
        return self._session.exec(select(Instructor).where(Instructor.id == instructor_id)).one_or_none()


    def get_all_instructors(self) -> Sequence[Instructor]:
            return self._session.exec(select(Instructor)).all()


    def update_instructor(self, instructor_id: int, data: UpdateUserSchema):
        instructor = self.get_instructor_by_id(instructor_id)
        if not instructor:
            return None
        instructor.first_name = data.first_name
        instructor.last_name = data.last_name
        instructor.email = data.email
        instructor.date_of_birth = data.date_of_birth

        self._session.add(instructor)
        self._session.commit()
        self._session.refresh(instructor)
        return instructor


    def delete_instructor(self, instructor_id: int) -> bool:
        instructor = self._session.exec(select(Instructor).where(Instructor.id == instructor_id)).one_or_none()
        if not instructor:
            return False
        self._session.delete(instructor)
        self._session.commit()
        return True


    def get_top_students(self, session: Session):
        # Build the query using SQLModel's select
        query = (
            select(
                Student.id,
                Student.userName,
                Student.firstName,
                Student.lastName,
                (
                    (Grade.pure_maths + Grade.chemistry + Grade.biology + Grade.computer_science + Grade.physics) / 5.0
                ).label('average_marks')
            )
            .join(Grade, Grade.student_id == Student.id)
            .order_by(desc('average_marks'))
            .limit(5)
        )
        
        # Execute the query and return the result
        top_students = session.exec(query).all()
        return top_students

    def add_new_grade(self, data: GradeSchema) -> Grade:
        grade = Grade(**dict(data))
        
        self._session.add(grade)
        self._session.commit()
        self._session.refresh(grade)
        
        return grade
    
    def update_grade(self, student_id: int, data: GradeSchema)-> Grade:
        grade = get_my_grades(student_id)
        if not grade:
            return None
        
        grade.student_id = student_id
        grade.pure_maths = data.pure_maths
        grade.chemistry = data.chemistry
        grade.biology = data.biology
        grade.computer_science = data.computer_science
        grade.physics = data.physics
        
        return grade 


    def view_grades(self, session: Session):
        query = session.exec(
            select(
                Student.id,
                Student.userName,
                Student.firstName,
                Student.lastName,
                Grade.pure_maths,
                Grade.chemistry,
                Grade.biology,
                Grade.computer_science,
                Grade.physics
            ).join(Grade, Student.id == Grade.student_id)  # Join grades with students
            .order_by(Student.id)  # Ordering by student ID
        )
        
        # Execute the query and return the result
        all_grades = query.all()

        # If no results, raise 204 No Content exception
        if not all_grades:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="No Records Found"  # Correct key is `detail`
            )
        
        return all_grades