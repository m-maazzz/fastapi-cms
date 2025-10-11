from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.event import EventOut, EventListResponse
from app.crud.event import event_crud
from app.core.database import get_db

event_router = APIRouter(prefix="/events", tags=["Events"])

@event_router.get("/", response_model=EventListResponse)
def list_events(
    page: int = 1,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit

    # Always fetch only published events (if you have is_published field, adjust accordingly)
    events, total = event_crud.get_all(
        db,
        ispublished=True,  # Adjust/remove if no is_published field on Event
        skip=skip,
        limit=limit
    )

    return EventListResponse(
        events=[EventOut.model_validate(event) for event in events],
        total=total,
        page=page,
        size=len(events)
    )


@event_router.get("/{id}", response_model=EventOut)
def get_event(id: int, db: Session = Depends(get_db)):
    event = event_crud.get(db, id)
    if not event or (hasattr(event, 'is_published') and not event.is_published):
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@event_router.get("/upcoming", response_model=EventListResponse)
def upcoming_events(page: int = 1, limit: int = 5, db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    events = event_crud.get_upcoming_events(db=db, skip=skip, limit=limit)
    total = len(events)  # or count query if needed

    return EventListResponse(
        events=[EventOut.model_validate(event) for event in events],
        total=total,
        page=page,
        size=len(events),
    )
