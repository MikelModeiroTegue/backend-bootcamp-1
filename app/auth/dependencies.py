from fastapi.security import OAuth2PasswordBearer
from app.data.models import Instructor, Student
from sqlmodel import Session, select
from passlib.context import CryptContext



#  set up the token url for obtaining the access token on successful authentication
oauth2_scheme_student = OAuth2PasswordBearer(
    tokenUrl = "auth/student",
    scheme_name= "Student Authentication",
    description= "Authentication endpoint for the students"
    )

oauth2_scheme_instructor = OAuth2PasswordBearer(
    tokenUrl= "auth/instructor",
    scheme_name= "Instructor Authentication",
    description= "Authentication endpoint for the Instructors"
    )

# Create a password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_instructor_by_name(self, instructor_name: str) -> Instructor | None:
        return self._session.exec(select(Instructor).where(Instructor.userName == instructor_name)).one_or_none()

    def get_student_by_name(self, student_name: str) -> Student | None:
        return self._session.exec(select(Student).where(Student.userName == student_name)).one_or_none()

    def authenticate_student(self, student_name: str, password: str):
        student = self.get_student_by_name(student_name)
        if not student:
            return False
        if not verify_password(password, student.hashed_password):
            return False
        return student

    def authenticate_instructor(self, instructor_name: str, password: str):
        instructor = self.get_instructor_by_name(instructor_name)
        if not instructor:
            return False
        if not verify_password(password, instructor.hashed_password):
            return False
        return instructor


# Utility functions outside the class
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
