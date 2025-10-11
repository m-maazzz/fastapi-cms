from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.core.database import Base
from app.models.base_mixin import TimestampMixin
import os
from app.core.config import settings
TABLE_PREFIX = settings.TABLE_PREFIX

class Event(Base, TimestampMixin):
    __tablename__ = f"{TABLE_PREFIX}events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    event_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    is_published = Column(Boolean, default=True)
    organizer_name = Column(String(100), nullable=False)
