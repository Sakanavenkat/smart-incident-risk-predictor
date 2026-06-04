from pydantic import BaseModel, EmailStr
from typing import Optional, List
import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Optional['UserOut'] = None


class TokenData(BaseModel):
    email: Optional[str] = None


class RoleOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str
    full_name: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    role: Optional[RoleOut] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TicketCreate(BaseModel):
    ticket_id: str
    priority: str
    category: str
    region: str
    assignment_group: str
    open_date: datetime.datetime
    sla_percentage: float
    status: str


class TicketOut(BaseModel):
    id: int
    ticket_id: str
    priority: str
    category: str
    region: str
    assignment_group: str
    open_date: datetime.datetime
    sla_percentage: float
    status: str
    open_days: Optional[int] = None

    class Config:
        from_attributes = True


class InvalidTicketRow(BaseModel):
    row_number: int
    error: str
    data: Optional[dict] = None


class UploadResponse(BaseModel):
    upload_id: int
    filename: str
    total_rows: int
    valid_rows: int
    invalid_rows: int
    success: bool
    message: str
    invalid_rows_detail: List[InvalidTicketRow] = []


class UploadHistoryOut(BaseModel):
    id: int
    filename: str
    total_rows: int
    valid_rows: int
    invalid_rows: int
    errors: Optional[str] = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class PredictionOut(BaseModel):
    id: int
    ticket_id: int
    predicted_label: str
    score: float
    model_version: Optional[str]

    class Config:
        from_attributes = True


Token.update_forward_refs()
