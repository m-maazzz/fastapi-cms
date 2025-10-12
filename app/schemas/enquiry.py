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


class TestimonialCreate(BaseModel):
    name: str
    designation: str | None = None
    content: str
    rating: int = 5

class TestimonialOut(TestimonialCreate):
    id: int
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TestimonialResponse(BaseModel):
    message: str = "Testimonial submitted successfully"
    data : list[TestimonialOut]
    
    class Config:
        from_attributes = True



class TestimonialUpdate(BaseModel):
    is_approved: bool

    class Config:
        from_attributes = True