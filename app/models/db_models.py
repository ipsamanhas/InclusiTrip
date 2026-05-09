from __future__ import annotations

import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.sqlite import JSON

from app.database import Base


class UserDB(Base):
    """SQLAlchemy model for the users table."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    accessibility_profile = Column(JSON, nullable=True)
