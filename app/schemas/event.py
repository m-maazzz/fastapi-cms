from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class EventBase(BaseModel):
    title: str
    slug: str
    description: str
    event_date: datetime
    location: Optional[str]
    image_url: Optional[str]
    is_published: bool = True
    organizer_name: str

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str]
    slug: Optional[str]
    description: Optional[str]
    event_date: Optional[datetime]
    location: Optional[str]
    image_url: Optional[str]
    is_published: Optional[bool]
    organizer_name: Optional[str]

class EventOut(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class EventListResponse(BaseModel):
    events: List[EventOut]
    total: int
    page: int
    size: int
