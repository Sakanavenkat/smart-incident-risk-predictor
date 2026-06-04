"""Database repository for User operations."""
from sqlalchemy.orm import Session
from backend.app import models, schemas
from backend.app.core.security import hash_password, verify_password


class UserRepository:
    """User data access layer."""

    @staticmethod
    def create_user(db: Session, user: schemas.UserCreate) -> models.User:
        """Create a new user in the database."""
        db_user = models.User(
            email=user.email,
            password_hash=hash_password(user.password),
            full_name=user.full_name,
            role_id=2,  # Default to 'user' role (id=2)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> models.User | None:
        """Retrieve user by email."""
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> models.User | None:
        """Retrieve user by ID."""
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
        """Retrieve all users with pagination."""
        return db.query(models.User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user_role(db: Session, user_id: int, role_id: int) -> models.User | None:
        """Update user role."""
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if db_user:
            db_user.role_id = role_id
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user."""
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
        """Authenticate user by email and password."""
        user = UserRepository.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user
