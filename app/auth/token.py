from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from app.data.schemas import Token

# Load SECRET_KEY from environment variables for better security
SECRET_KEY = os.getenv("SECRET_KEY", "58e2fba902c292b2d16cee5dc4280359ffa66218d08ab32d1720492be3069bdf")

'''Secret Key Management:
I used os.getenv("SECRET_KEY", default_value) to load the secret key from environment variables. 
If the environment variable is not set, it defaults to your existing hardcoded key.'''
ALGORITHM = "HS256"

# Create a password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=5)
    
    # Convert the datetime to a UNIX timestamp before encoding
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt_token

# Function to verify a token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        role: str = payload.get("role") # Extract the subject (usually username)
        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: subject not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload  # Optionally return the payload if verification is successful
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
