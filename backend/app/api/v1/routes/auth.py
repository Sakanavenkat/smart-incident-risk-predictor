from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from backend.app import schemas
from backend.app.core.jwt import create_access_token
from backend.app.db.session import get_db
from backend.app.repositories.user_repo import UserRepository
from backend.app.services.user_service import UserService
from backend.app.core.security import hash_password

router = APIRouter()


@router.post("/register", response_model=schemas.UserOut)
def register(user_data: schemas.UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Requirements:
    - email: valid email address
    - password: at least 8 characters
    - password_confirm: must match password
    - full_name: optional
    """
    # Validate password length
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )
    
    # Validate password confirmation
    if user_data.password != user_data.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    # Check if user already exists
    existing_user = UserRepository.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    # Create user
    user_create = schemas.UserCreate(
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name
    )
    user = UserRepository.create_user(db, user_create)
    return schemas.UserOut.from_orm(user)


@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password.
    
    Returns:
    - access_token: JWT token for subsequent requests
    - token_type: Bearer
    - expires_in: token expiration time in seconds
    - user: user information
    """
    # Authenticate user
    user = UserRepository.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=60)
    token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 3600,
        "user": schemas.UserOut.from_orm(user)
    }


@router.post("/logout")
def logout():
    """
    Logout endpoint.
    
    Note: JWT is stateless, so logout is primarily a client-side operation.
    The client should discard the token.
    """
    return {"message": "Logged out successfully"}
