# app/routers/event.py

from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate, EventUpdate, EventOut, EventListResponse
from app.crud.event import event_crud
from app.core.database import get_db
from app.core.security import AuthService   
from app.utlis.file_handler import save_upload_file
from slugify import slugify
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/events", tags=["Events Admin"])
auth_service = AuthService()

# ---- Public Routes ----
@router.get("/", response_model=EventListResponse)
def list_events_admin(
    page: int = 1,
    limit: int = 5,
    is_published: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user=Depends(auth_service.get_current_user)
):
    skip = (page - 1) * limit
    if is_published is not None:
        events, total = event_crud.get_all(db, is_published=is_published, skip=skip, limit=limit)
    else:
        events, total = event_crud.get_all(db, skip=skip, limit=limit)

    return EventListResponse(
        events=[EventOut.model_validate(event) for event in events],
        total=total,
        page=page,
        size=len(events)
    )

# ---- Admin Routes ----
@router.post("/", response_model=EventOut)
def create_event(
    title: str = Form(...),
    description: str = Form(...),
    event_date: str = Form(...),  # ISO format string
    location: Optional[str] = Form(None),
    is_published: bool = Form(True),
    organizer_name: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_admin=Depends(auth_service.get_current_user)
):
    image_url = None
    if image:
        image_url = save_upload_file(image, subfolder="events")

    slug = slugify(title)
    event_date_parsed = datetime.fromisoformat(event_date)

    event_data = EventCreate(
        title=title,
        slug=slug,
        description=description,
        event_date=event_date_parsed,
        location=location,
        image_url=image_url,
        is_published=is_published,
        organizer_name=organizer_name
    )

    created_event = event_crud.create(db, event_data)
    return created_event

@router.put("/{event_id}", response_model=EventOut)
def update_event(
    event_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    event_date: Optional[str] = Form(None),  # ISO date string or None
    location: Optional[str] = Form(None),
    is_published: Optional[bool] = Form(None),
    organizer_name: Optional[str] = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_admin=Depends(auth_service.get_current_user)
):
    update_data = {}

    if title is not None:
        update_data['title'] = title
        update_data['slug'] = slugify(title)
    if description is not None:
        update_data['description'] = description
    if event_date is not None:
        update_data['event_date'] = datetime.fromisoformat(event_date)
    if location is not None:
        update_data['location'] = location
    if is_published is not None:
        update_data['is_published'] = is_published
    if organizer_name is not None:
        update_data['organizer_name'] = organizer_name
    if image:
        update_data['image_url'] = save_upload_file(image, subfolder="events")

    db_event = event_crud.get(db, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    event_update = EventUpdate(**update_data)
    updated_event = event_crud.update(db, db_event, event_update)
    return updated_event


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(auth_service.get_current_user)
):
    deleted = event_crud.delete(db, event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}
