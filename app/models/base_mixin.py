from sqlalchemy import Column, DateTime
from datetime import datetime
from sqlalchemy.sql import func

class TimestampMixin:
    """Adds created_at and updated_at columns to any model."""
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(), onupdate=lambda: datetime.now(), nullable=False)