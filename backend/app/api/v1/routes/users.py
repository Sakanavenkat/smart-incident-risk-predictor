"""User management endpoints (admin only)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app import schemas
from backend.app.db.session import get_db
from backend.app.core.dependencies import require_admin
from backend.app.services.user_service import UserService
from backend.app.repositories.user_repo import UserRepository

router = APIRouter()


@router.get("/me", response_model=schemas.UserOut)
def get_current_user(
    current_user = Depends(lambda: None),
    db: Session = Depends(get_db)
):
    """Get current logged-in user info."""
    from backend.app.core.dependencies import get_current_user_from_header
    from fastapi import Header
    
    auth_header = None  # This would come from request headers in real implementation
    user = get_current_user_from_header(auth_header, db) if auth_header else None
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    return schemas.UserOut.from_orm(user)


@router.get("/", response_model=list[schemas.UserOut])
def list_users(
    current_user = Depends(require_admin),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all users (admin only).
    
    Query params:
    - skip: number of records to skip (default: 0)
    - limit: maximum number of records to return (default: 100)
    """
    users = UserService.list_users(db, skip, limit)
    return users


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(
    user_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only)."""
    user = UserRepository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return schemas.UserOut.from_orm(user)


@router.put("/{user_id}/role", response_model=schemas.UserOut)
def update_user_role(
    user_id: int,
    role_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Update user role (admin only).
    
    Role IDs:
    - 1: Admin
    - 2: Manager
    - 3: User
    """
    # Validate role_id
    if role_id not in (1, 2, 3):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role_id. Use 1 (Admin), 2 (Manager), or 3 (User)"
        )
    
    user = UserService.update_user_role(db, user_id, role_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a user (admin only)."""
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}
