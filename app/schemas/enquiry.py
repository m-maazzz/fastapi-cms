from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    message: str

class ContactOut(ContactCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ContactResponse(BaseModel):
    message: str = "Contact form submitted successfully"
    data : list[ContactOut]
    
    class Config:
        from_attributes = True
