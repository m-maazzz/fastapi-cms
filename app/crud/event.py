from typing import Any, Dict, List, Optional, Callable
from sqlalchemy.orm import Session, Query
from sqlalchemy import asc, desc
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate
from app.crud.base import CRUDBase
from datetime import date
class EventCRUD(CRUDBase[Event, EventCreate, EventUpdate]):
    def __init__(self, model):
        super().__init__(model)
    
    def get_upcoming_events(
    self, db: Session, from_date: date = None, skip: int = 0, limit: int = 10
    ):
        if not from_date:
            from_date = date.today()
        query = db.query(self.model).filter(self.model.event_date >= from_date)
        query = query.order_by(asc(self.model.event_date))
        return query.offset(skip).limit(limit).all()

event_crud = EventCRUD(Event)
