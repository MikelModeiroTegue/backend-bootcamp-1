import sqlite3
from typing import Annotated

from jose import ExpiredSignatureError
from jwt import InvalidTokenError
from sqlmodel import Session
from app.auth.dependencies import oauth2_scheme_instructor, oauth2_scheme_student
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from app.auth.token import verify_token
from app.api.dependencies import get_repo
from app.data.models import Grade
from app.data.student_repo import AbstractRepo
from app.data.schemas import CreateUserSchema, GetInstructorResponse, GetInstructorsResponse, GradeSchema, TokenData, UpdateInstructorResponse, UpdateUserSchema, UserSchema, GetStudentsResponse, \
    UpdateStudentResponse, GetStudentResponse
from app.domain import instructor_service, student_service
from app.auth.dependencies import UserRepository, hash_password

router = APIRouter(prefix="/api")


@router.post("/create-user", response_model=UserSchema)  # Creation of a student
def create_User(
    user: CreateUserSchema,
    repo: Annotated[AbstractRepo, Depends(get_repo)],
    token: Annotated[str, Depends(oauth2_scheme_instructor)],
    session: Session
):
    payload = verify_token(token)
    userRepo = UserRepository(session)
    instructor = userRepo.get_instructor_by_name(payload.get("username"))
    
    if instructor is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            details = "Couldn't Find this instructor",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    hashed_passwd = hash_password(user.password)
    
    if user.userRole == "Student":
    
        user_data = user.model_dump()
        user_data["hashed_password"] = hashed_passwd
        
        student = student_service.create_student(data=user_data, user_repo=repo)
        try:
            return UserSchema.model_validate(dict(student))  # Use model_validate to create a UserSchema instance
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))  # Handle validation errors
    
    elif user.user_role == "Instructor":
        user_data = user.model_dump()
        user_data["hashed_password"] = hashed_passwd
        
        instructor = instructor_service.create_instructor(data=user_data, user_repo=repo)
        try:
            return UserSchema.model_validate(dict(instructor))  # Use model_validate to create a UserSchema instance
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))  # Handle validation errors
        


@router.get("/students", response_model=GetStudentsResponse)  # Get all students
def get_students(
    repo: Annotated[AbstractRepo, Depends(get_repo)],
    token: Annotated[str, Depends(oauth2_scheme_instructor)],
    session: Session
):
    payload = verify_token(token)
    userRepo = UserRepository(session)
    instructor = userRepo.get_instructor_by_name(payload.get("username"))
    
    if instructor is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            details = "Couldn't Find this instructor",
            headers={"WWW-Authenticate": "Bearer"}
        )
    # Operation
    students = student_service.get_students(repo)
    return GetStudentsResponse(students=students)


@router.get("/students/{user_id}", response_model=GetStudentResponse)  # Get student by id
def get_student_by_id(
    user_id: int,
    repo: Annotated[AbstractRepo, Depends(get_repo)],
    token: Annotated[str, Depends(oauth2_scheme_instructor)],
    session: Session
):
    payload = verify_token(token)
    userRepo = UserRepository(session)
    instructor = userRepo.get_instructor_by_name(payload.get("username"))
    
    if instructor is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            details = "Couldn't Find this instructor",
            headers={"WWW-Authenticate": "Bearer"}
        )
    student = student_service.get_student(student_id=user_id, user_repo=repo)
    try:
        return GetStudentResponse.model_validate(dict(student))  # Use model_validate to create a UserSchema instance
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # Handle validation errors


@router.put("/students/{user_id}", response_model=UpdateStudentResponse)  # Update a student
def update_student(
    user_id: int,
    schema: UpdateUserSchema,
    repo: Annotated[AbstractRepo, Depends(get_repo)],
    session: Session,
    token: Annotated[str, Depends(oauth2_scheme_instructor)]
):
    payload = verify_token(token)
    userRepo = UserRepository(session)
    instructor = userRepo.get_instructor_by_name(payload.get("username"))
    
    if instructor is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            details = "Couldn't Find this instructor",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    student = student_service.update_student(student_id=user_id, repo=repo, data=schema)
    try:
        return UpdateStudentResponse.model_validate(dict(student))  # Use model_validate to create a UserSchema instance
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # Handle validation errors


@router.delete("/students/{user_id}", status_code=204)  # Delete a student
def delete_student(
    user_id: int,
    repo: Annotated[AbstractRepo, Depends(get_repo)],
    session = Session, 
    token = Annotated[str, Depends(oauth2_scheme_instructor)]
):
    payload = verify_token(token)
    userRepo = UserRepository(session)
    instructor = userRepo.get_instructor_by_name(payload.get("username"))
    
    if instructor is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            details = "Couldn't Find this instructor",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    student_service.delete_student(student_id=user_id, repo=repo)
    return {"student deleted successfully"}



@router.get("/instructor/{instructor_id}", response_model=GetInstructorResponse)  # Get instructor by id
def get_instructor_by_id(
    instructor_id: int,
    repo: Annotated[AbstractRepo, Depends(get_repo)],
    token: Annotated[str, Depends(oauth2_scheme_instructor)],
    session: Session
):
    payload = verify_token(token)
    userRepo = UserRepository(session)
    instructor = userRepo.get_instructor_by_name(payload.get("username"))
    
    if instructor is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            details = "Couldn't Find this instructor",
            headers={"WWW-Authenticate": "Bearer"}
        )
    instructor = instructor_service.get_instructor(instructor_id=instructor_id, user_repo=repo)
    try:
        return GetInstructorResponse.model_validate(dict(instructor))  # Use model_validate to create a UserSchema instance
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # Handle validation errors


@router.get("/instructors", response_model=GetInstructorsResponse)  # Get all instructors
def get_instructors(
    repo: Annotated[AbstractRepo, Depends(get_repo)],
    token: Annotated[str, Depends(oauth2_scheme_instructor)],
    session: Session
):
    payload = verify_token(token)
    userRepo = UserRepository(session)
    instructor = userRepo.get_instructor_by_name(payload.get("username"))
    
    if instructor is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            details = "Couldn't Find this instructor",
            headers={"WWW-Authenticate": "Bearer"}
        )
    # Operation
    instructors = instructor_service.get_instructor(repo)
    return GetInstructorsResponse(instructors=instructors)


@router.put("/instructor/{instructor_id}", response_model=UpdateStudentResponse)  # Update a student
def update_instructor(
    instructor_id: int,
    schema: UpdateUserSchema,
    repo: Annotated[AbstractRepo, Depends(get_repo)],
    session: Session,
    token: Annotated[str, Depends(oauth2_scheme_instructor)]
):
    payload = verify_token(token)
    userRepo = UserRepository(session)
    instructor = userRepo.get_instructor_by_name(payload.get("username"))
    
    if instructor is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            details = "Couldn't Find this instructor",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    instructor = instructor_service.update_instructor(instructor_id=instructor_id, repo=repo, data=schema)
    try:
        return UpdateInstructorResponse.model_validate(dict(instructor))  # Use model_validate to create a UserSchema instance
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # Handle validation errors



@router.delete("/instructor/{user_id}", status_code=204)  # Delete a student
def delete_instructor(
    user_id: int,
    repo: Annotated[AbstractRepo, Depends(get_repo)],
    session = Session, 
    token = Annotated[str, Depends(oauth2_scheme_instructor)]
):
    payload = verify_token(token)
    userRepo = UserRepository(session)
    instructor = userRepo.get_instructor_by_name(payload.get("username"))
    
    if instructor is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            details = "Couldn't Find this instructor",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    instructor_service.delete_instructor(instructor_id = user_id, repo = repo)
    
    return {"deleted successfully"}


@router.get("/my-grades", 
         response_model = Grade, 
         tags = ["Students' Endpoints"], 
         description="Student view his/her grades",
         summary="Student view his/her grades")
async def get_student_grade(student_name: str , token: Annotated[str, Depends(oauth2_scheme_student)], session: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)

        if not payload:
            raise HTTPException(
                status_code= status.HTTP_204_NO_CONTENT,
                details= "No Token Found",
                headers= {"WWW-Authenticate": "Bearer"}
            )
        username = payload.get("username")
        if username == student_name:
            token_D = {
                "username": username,
                "role": payload.get("role")
            }
            token_data = TokenData(**token_D)
        
        # if the username in the token doesn't match the student_name parameter provided in the request
        if username != student_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this student's grade",
                )

    except InvalidTokenError:
        raise credentials_exception
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
            )
    
    userRepo = UserRepository(session)
    student = userRepo.get_student_by_name(username = token_data.username)
    
    if student is None:
        raise credentials_exception
    
    Student_grades = student_service.get_my_grades(student_id = student.id)
    
    # Handling the error condition for null value of the Student_grades
    if Student_grades is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No grades found for this student"
        )
    return Student_grades


@router.get("/top-students", 
        tags = ["Instructor"], 
        description="Get the top 5 students by an Authorized instructor",
        summary="Retrieve the top 5 most performant student")
async def top_students(token: Annotated[str, Depends(oauth2_scheme_instructor)], session: Session):
    
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    try:
        payload = verify_token(token)
        userRepo = UserRepository(session)
        instructor = userRepo.get_instructor_by_name(payload.get("username"))
        # UnAuthorized token sent is not granted the permission to use this endpoint

        if instructor is None:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                details = "Couldn't Find this instructor",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Perform operation here
        
        topStudents = instructor_service.get_top_students()

        return topStudents
    
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A student Records not found")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error: " + str(e))
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
            )


@router.put("/students/grades/update-Add", 
         response_model= Grade, 
         tags = ["Instructor"], 
         description="Update Existing Student Marks by an Authorized instructor",
         summary="Update existing Records of Students")
async def update_or_Add_student_Record(student_id: int, grade: GradeSchema, token: Annotated[str, Depends(oauth2_scheme_instructor)], session: Session):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        userRepo = UserRepository(session)
        instructor = userRepo.get_instructor_by_name(payload.get("username"))
        # UnAuthorized token sent is not granted the permission to use this endpoint

        if instructor is None:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                details = "Couldn't Find this instructor",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # operation 
        
        existing_student= student_service.get_student(student_id)
        if not existing_student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student with the ID provided not found")
        
        # check if the student has grades in the grade table
        existing_student_grade = student_service.get_my_grades(student_id)
        
        if existing_student_grade:
            # Update the student grades if already existing
            update_grade = instructor_service.update_grade(student_id = student_id, data= grade)
            
            return update_grade
        
        else:
            new_grade = instructor_service.add_new_grade(data = grade)
            
            return new_grade
    
    except InvalidTokenError:
            raise credentials_exception
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
            )
    except sqlite3.IntegrityError as e:
    # Check if it's a CHECK constraint violation
        if 'CHECK constraint failed' in str(e):
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Grade value exceeds the allowed range (0-20).")
    


@router.get("/all-grades", 
        tags = ["Instructor"], 
        description="Get all the students with their grade records",
        summary="get all student grades")
async def view_grades(token: Annotated[str, Depends(oauth2_scheme_instructor)], session: Session):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        userRepo = UserRepository(session)
        instructor = userRepo.get_instructor_by_name(payload.get("username"))
        # UnAuthorized token sent is not granted the permission to use this endpoint

        if instructor is None:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                details = "Couldn't Find this instructor",
                headers={"WWW-Authenticate": "Bearer"}
            )
        #  OPeration performed 
        
        all_grades = instructor_service.view_all_grades()
        
        if not all_grades:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND, 
                detail="No record Found")
        
        return all_grades
    
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A student Records not found")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error: " + str(e))
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
            )