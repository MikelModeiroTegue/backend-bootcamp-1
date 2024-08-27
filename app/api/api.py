from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from app.api.dependencies import get_repo
from app.data.repo import AbstractRepo
from app.data.schemas import CreateStudentSchema, UpdateStudentSchema, CreateStudentResponse, GetStudentsResponse, \
    UpdateStudentResponse, GetStudentResponse
from app.domain import student_service

router = APIRouter(prefix="/api")


@router.post("/students", response_model=CreateStudentResponse)  # Creation of a student
def create_student(
    schema: CreateStudentSchema,
    repo: Annotated[AbstractRepo, Depends(get_repo)]
):
    student = student_service.create_student(data=schema, user_repo=repo)
    return CreateStudentResponse(**dict(student))


@router.get("/students", response_model=GetStudentsResponse)  # Get all students
def get_students(
    repo: Annotated[AbstractRepo, Depends(get_repo)]
):
    students = student_service.get_students(repo)
    return GetStudentsResponse(students=students)


@router.get("/students/{user_id}", response_model=GetStudentResponse)  # Get student by id
def get_student_by_id(
    user_id: int,
    repo: Annotated[AbstractRepo, Depends(get_repo)]
):
    student = student_service.get_student(student_id=user_id, user_repo=repo)
    return GetStudentResponse(**dict(student))


@router.put("/students/{user_id}", response_model=UpdateStudentResponse)  # Update a student
def update_student(
    user_id: int,
    schema: UpdateStudentSchema,
    repo: Annotated[AbstractRepo, Depends(get_repo)]
):
    student = student_service.update_student(student_id=user_id, repo=repo, data=schema)
    return UpdateStudentResponse(**dict(student))


@router.delete("/students/{user_id}", status_code=204)  # Delete a student
def delete_student(
    user_id: int,
    repo: Annotated[AbstractRepo, Depends(get_repo)]
):
    student_service.delete_student(student_id=user_id, repo=repo)
