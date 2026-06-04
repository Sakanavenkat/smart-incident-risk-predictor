"""Database seeding utilities for initial setup."""
from sqlalchemy.orm import Session
from backend.app import models
from backend.app.core.security import hash_password


def seed_roles(db: Session):
    """Create default roles if they don't exist."""
    roles = [
        {"id": 1, "name": "admin"},
        {"id": 2, "name": "manager"},
        {"id": 3, "name": "user"},
    ]
    
    for role_data in roles:
        existing_role = db.query(models.Role).filter(models.Role.id == role_data["id"]).first()
        if not existing_role:
            role = models.Role(id=role_data["id"], name=role_data["name"])
            db.add(role)
    
    db.commit()


def seed_admin_user(db: Session):
    """Create default admin user if it doesn't exist."""
    admin_email = "admin@example.com"
    existing_user = db.query(models.User).filter(models.User.email == admin_email).first()
    
    if not existing_user:
        admin_user = models.User(
            email=admin_email,
            password_hash=hash_password("Admin@123456"),  # Change in production!
            full_name="Administrator",
            role_id=1  # Admin role
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print(f"✓ Admin user created: {admin_email} / Admin@123456")
    else:
        print(f"✓ Admin user already exists: {admin_email}")


def seed_sample_users(db: Session):
    """Create sample users for testing."""
    sample_users = [
        {
            "email": "manager@example.com",
            "password": "Manager@123456",
            "full_name": "Sample Manager",
            "role_id": 2
        },
        {
            "email": "user@example.com",
            "password": "User@123456",
            "full_name": "Sample User",
            "role_id": 3
        }
    ]
    
    for user_data in sample_users:
        existing_user = db.query(models.User).filter(models.User.email == user_data["email"]).first()
        if not existing_user:
            user = models.User(
                email=user_data["email"],
                password_hash=hash_password(user_data["password"]),
                full_name=user_data["full_name"],
                role_id=user_data["role_id"]
            )
            db.add(user)
    
    db.commit()
    print("✓ Sample users created")


def init_database(db: Session):
    """Initialize database with default data."""
    print("Initializing database...")
    seed_roles(db)
    seed_admin_user(db)
    seed_sample_users(db)
    print("Database initialization complete!")
