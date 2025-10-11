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
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    is_published: Optional[bool] = None
    organizer_name: Optional[str] = None

class EventOut(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EventListResponse(BaseModel):
    events: List[EventOut]
    total: int
    page: int
    size: int
