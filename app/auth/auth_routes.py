# 13 the instructors' token route
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.dependencies import UserRepository
from app.data.schemas import Token
from sqlmodel import Session, select
from app.auth.token import create_access_token


router = APIRouter(prefix="/auth")
ACCESS_TOKEN_EXPIRATION_TIMEOUT = 45


#  Authenticate Endpoint for the Instructors 
@router.post("/instructor", 
        response_model = Token, 
        tags = ["Authentication Endpoints"], 
        description=" Implement token-based authentication",
        summary= "Authenticates an Instructor in the system")
async def get_instructor_access_token (session: Session, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Access the username, password, from the form_data object
    username = form_data.username
    password = form_data.password
# Add your authentication logic here, that's validating instructor credentials
    user_repo = UserRepository(session)
    instructor = user_repo.authenticate_instructor(username, password)
    
    if not instructor: 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Invalid credentials", 
            headers = {"WWW-Authenticate":"Bearer"}
            )
    
    # define the expiration time on successful authentication 
    access_token_expiration_time = timedelta(minutes = ACCESS_TOKEN_EXPIRATION_TIMEOUT)
    
    #  create the access token 
    access_token = create_access_token(
        data = {
            "username": username,
            "role": instructor.userRole },
        expires_delta = access_token_expiration_time
        )
    #response 
    return Token(
        access_token = access_token,
        token_type = "Bearer",
        role = instructor.userRole
    )


#  Authenticate Endpoint for the Students 
@router.post("/students", 
        response_model = Token, 
        tags = ["Authentication Endpoints"], 
        description=" Implement token-based authentication",
        summary= "Authenticates a Student in the system")
async def get_student_access_token (session: Session, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Access the username, password, from the form_data object
    username = form_data.username
    password = form_data.password
# Add your authentication logic here, that's validating instructor credentials
    user_repo = UserRepository(session)
    student = user_repo.authenticate_student(username, password)
    
    if not student: 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Invalid credentials", 
            headers = {"WWW-Authenticate":"Bearer"}
            )
    
    # define the expiration time on successful authentication 
    access_token_expiration_time = timedelta(minutes = ACCESS_TOKEN_EXPIRATION_TIMEOUT)
    
    #  create the access token 
    access_token = create_access_token(
        data = {
            "username": username,
            "role": student.userRole },
        expires_delta = access_token_expiration_time
        )
    #response 
    return Token(
        access_token = access_token,
        token_type = "Bearer",
        role = student.userRole
    )