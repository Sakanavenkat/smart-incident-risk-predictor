"""User service layer - business logic for user operations."""
from sqlalchemy.orm import Session
from backend.app import schemas
from backend.app.repositories.user_repo import UserRepository


class UserService:
    """User business logic service."""

    @staticmethod
    def register_user(db: Session, user: schemas.UserCreate) -> schemas.UserOut:
        """Register a new user."""
        # Check if user already exists
        existing_user = UserRepository.get_user_by_email(db, user.email)
        if existing_user:
            raise ValueError(f"User with email {user.email} already exists")
        
        db_user = UserRepository.create_user(db, user)
        return schemas.UserOut.from_orm(db_user)

    @staticmethod
    def get_user(db: Session, user_id: int) -> schemas.UserOut | None:
        """Get user by ID."""
        user = UserRepository.get_user_by_id(db, user_id)
        if user:
            return schemas.UserOut.from_orm(user)
        return None

    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.UserOut]:
        """List all users."""
        users = UserRepository.get_all_users(db, skip, limit)
        return [schemas.UserOut.from_orm(user) for user in users]

    @staticmethod
    def update_user_role(db: Session, user_id: int, role_id: int) -> schemas.UserOut | None:
        """Update user role (admin only)."""
        user = UserRepository.update_user_role(db, user_id, role_id)
        if user:
            return schemas.UserOut.from_orm(user)
        return None

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user (admin only)."""
        return UserRepository.delete_user(db, user_id)
