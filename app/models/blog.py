from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base_mixin import TimestampMixin
import os
TABLE_PREFIX = os.getenv("TABLE_PREFIX", "")  

class Blog(Base, TimestampMixin):
    __tablename__ = f"{TABLE_PREFIX}blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(255), nullable=True)
    is_published = Column(Boolean, default=True)
    author_name = Column(String(100), nullable=False)
