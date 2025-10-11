from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base
from sqlalchemy.orm import relationship
import os
TABLE_PREFIX = os.getenv("TABLE_PREFIX", "")
class User(Base):
    __tablename__ = f"{TABLE_PREFIX}blogs"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
