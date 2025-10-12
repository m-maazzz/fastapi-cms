from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime, timezone
from app.core.database import Base
from app.core.config import settings

TABLE_PREFIX = settings.TABLE_PREFIX

class ContactForm(Base):
    __tablename__ = f"{TABLE_PREFIX}contact_forms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
