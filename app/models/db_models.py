from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship

from app.database import Base


class UserDB(Base):
    """SQLAlchemy model for the users table."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    phone = Column(String(64), nullable=True)
    photo_url = Column(Text, nullable=True)
    accessibility_profile = Column(JSON, nullable=True)


class HotelDB(Base):
    """SQLAlchemy model for hotel listings."""

    __tablename__ = "hotels"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String(36), ForeignKey("hotel_owners.id"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)
    accessibility_features = Column(JSON, nullable=False)

    reviews = relationship(
        "ReviewDB",
        back_populates="hotel",
        cascade="all, delete-orphan",
    )
    owner = relationship("HotelOwnerDB", back_populates="hotels")


class HotelOwnerDB(Base):
    """SQLAlchemy model for future hotel-owner accounts."""

    __tablename__ = "hotel_owners"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_name = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    phone = Column(String(64), nullable=True)

    hotels = relationship("HotelDB", back_populates="owner")


class ReviewDB(Base):
    """SQLAlchemy model for hotel accessibility reviews."""

    __tablename__ = "reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=True)
    hotel_id = Column(String(36), ForeignKey("hotels.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    accessibility_category = Column(String(64), nullable=False)
    comment = Column(Text, nullable=False)

    hotel = relationship("HotelDB", back_populates="reviews")


class SearchDB(Base):
    """Stored search request for logged-in users."""

    __tablename__ = "searches"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    destination = Column(String(255), nullable=False, index=True)
    guests = Column(Integer, nullable=False, default=1)
    accessibility_needs = Column(JSON, nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
