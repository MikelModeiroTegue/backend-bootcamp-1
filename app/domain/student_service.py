from typing import Any

from fastapi import HTTPException, status

from app.data.models import Student
from app.data.student_repo import AbstractRepo
from app.data.schemas import CreateUserSchema, UpdateUserSchema
from app.domain.exceptions import StudentNotFound


def create_student(
    data: CreateUserSchema,
    user_repo: AbstractRepo
) -> Student:
    user = user_repo.create_student(data=data)
    return user


def get_students(user_repo: AbstractRepo) -> list[dict[str, Any]]:
    students = user_repo.get_all_students()
    return [dict(student) for student in students]


def get_student(student_id: int, user_repo: AbstractRepo) -> Student:
    user = user_repo.get_student_by_id(user_id=student_id)
    if not user:
        raise StudentNotFound(title="Not Found", message=f"Student with id {student_id} not found")
    return user


def update_student(
    student_id: int,
    data: UpdateUserSchema,
    repo: AbstractRepo
) -> Student:
    user = repo.update_student(user_id=student_id, data=data)
    if not user:
        raise StudentNotFound
    return user


def delete_student(student_id: int, repo: AbstractRepo):
    has_been_deleted = repo.delete_student(user_id=student_id)
    if not has_been_deleted:
        raise StudentNotFound

def get_my_grades(student_id: int, repo: AbstractRepo):
    grade = repo.get_my_grades(student_id)
    if not grade:
        raise HTTPException (
                status_code= status.HTTP_204_NO_CONTENT, 
                details = "No Content was Found",
                headers = {"WWW-Authenticate":"Bearer"}
            )
    return grade