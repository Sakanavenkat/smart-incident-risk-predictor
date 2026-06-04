"""Role-based access control and authentication dependencies."""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.jwt import decode_token
from backend.app.db.session import get_db
from backend.app.repositories.user_repo import UserRepository


async def get_current_user(
    token: str = Depends(lambda: None),
    db: Session = Depends(get_db)
):
    """Get current authenticated user from JWT token."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    email = payload.get("sub")
    user = UserRepository.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


async def require_admin(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Require admin role."""
    user = current_user
    if not user or user.role_id != 1:  # 1 = admin role
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user


async def require_manager_or_admin(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Require manager or admin role."""
    user = current_user
    if not user or user.role_id not in (1, 2):  # 1=admin, 2=manager
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager or Admin access required"
        )
    return user


def get_current_user_from_header(
    authorization: str | None = None,
    db: Session = Depends(get_db)
):
    """Extract and validate user from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = authorization.split("Bearer ")[1]
    payload = decode_token(token)
    
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    email = payload.get("sub")
    user = UserRepository.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user
