from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String(255), unique=True, index=True, nullable=False)
    priority = Column(String(50))
    category = Column(String(255))
    region = Column(String(255))
    assignment_group = Column(String(255))
    open_date = Column(DateTime)
    sla_percentage = Column(Float)
    status = Column(String(50))
    open_days = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    predicted_label = Column(String(50))
    score = Column(Float)
    model_version = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AlertLog(Base):
    __tablename__ = "alert_logs"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    risk_level = Column(String(50))
    sent_to = Column(String(255))
    status = Column(String(50))
    payload = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class UploadHistory(Base):
    __tablename__ = "upload_history"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    total_rows = Column(Integer)
    valid_rows = Column(Integer)
    invalid_rows = Column(Integer)
    errors = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
