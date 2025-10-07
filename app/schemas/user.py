from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class UserData(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    message: str
    data: UserData
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
