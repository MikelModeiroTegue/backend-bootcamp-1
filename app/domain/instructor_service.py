from typing import Any

from fastapi import HTTPException, status
from sqlmodel import Session

from app.data.models import Grade, Instructor
from app.data.instructor_repo import AbstractRepo
from app.data.schemas import CreateUserSchema, GradeSchema, UpdateUserSchema
from app.domain.exceptions import InstructorNotFound


def create_instructor(
    data: CreateUserSchema,
    user_repo: AbstractRepo
) -> Instructor:
    user = user_repo.create_instructor(data=data)
    return user


def get_instructors(user_repo: AbstractRepo) -> list[dict[str, Any]]:
    instructors = user_repo.get_all_instructors()
    return [dict(instructor) for instructor in instructors]


def get_instructor(instructor_id: int, user_repo: AbstractRepo) -> Instructor:
    user = user_repo.get_instructor_by_id(user_id=instructor_id)
    if not user:
        raise InstructorNotFound(title="Not Found", message=f"Instructor with id {instructor_id} not found")
    return user


def update_instructor(
    instructor_id: int,
    data: UpdateUserSchema,
    repo: AbstractRepo
) -> Instructor:
    user = repo.update_instructor(user_id=instructor_id, data=data)
    if not user:
        raise InstructorNotFound
    return user


def delete_instructor(instructor_id: int, repo: AbstractRepo):
    has_been_deleted = repo.delete_instructor(user_id=instructor_id)
    if not has_been_deleted:
        InstructorNotFound


def get_top_students(repo: AbstractRepo):
    top_students = repo.get_top_students()
    if not top_students:
        raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                details= "No Records Found"
            )
    return [dict(top_student) for top_student in top_students]

def add_new_grade(data: GradeSchema, repo: AbstractRepo)-> Grade:
    grade = repo.add_new_grade(data)
    return grade

def update_grade(data: GradeSchema, repo: AbstractRepo, student_id: int)-> Grade:
    grade = repo.update_grade(student_id, data)
    
    return grade


def view_all_grades(repo: AbstractRepo, session: Session):
    # Pass session to repo method
    all_grades = repo.view_grades(session=session)
    
    return [
        {
            "id": grade.id,  # Accessing by field name, not index
            "userName": grade.userName,
            "firstName": grade.firstName,
            "lastName": grade.lastName,
            "grades": {
                "pure_maths": grade.pure_maths,
                "chemistry": grade.chemistry,
                "biology": grade.biology,
                "computer_science": grade.computer_science,
                "physics": grade.physics
            }
        } for grade in all_grades
    ]