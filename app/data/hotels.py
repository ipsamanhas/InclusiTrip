from __future__ import annotations

import uuid
from typing import List

from sqlalchemy.orm import Session, selectinload

from app.models.db_models import HotelDB
from app.models.models import Hotel, HotelAccessibilityFeatures, Review


def db_hotel_to_model(hotel: HotelDB) -> Hotel:
    """Convert a SQLAlchemy hotel row into the Pydantic model used by matching."""
    return Hotel(
        id=uuid.UUID(str(hotel.id)),
        name=hotel.name,
        email=hotel.email,
        password=hotel.password or "",
        location=hotel.location,
        description=hotel.description,
        rating=hotel.rating,
        accessibility_features=HotelAccessibilityFeatures.model_validate(
            hotel.accessibility_features
        ),
        reviews=[
            Review(
                id=uuid.UUID(str(review.id)),
                user_id=uuid.UUID(str(review.user_id)) if review.user_id else None,
                hotel_id=uuid.UUID(str(review.hotel_id)),
                rating=review.rating,
                accessibility_category=review.accessibility_category,
                comment=review.comment,
            )
            for review in hotel.reviews
        ],
    )


def list_hotels(db: Session) -> List[Hotel]:
    """Return all hotel listings from the database."""
    hotel_rows = (
        db.query(HotelDB)
        .options(selectinload(HotelDB.reviews))
        .order_by(HotelDB.name)
        .all()
    )
    return [db_hotel_to_model(hotel) for hotel in hotel_rows]


def get_hotel_by_id(db: Session, hotel_id: str) -> HotelDB | None:
    """Look up one hotel listing by id."""
    return (
        db.query(HotelDB)
        .options(selectinload(HotelDB.reviews))
        .filter(HotelDB.id == hotel_id)
        .first()
    )


def get_hotel_by_email(db: Session, email: str) -> HotelDB | None:
    """Look up a hotel account by email."""
    return db.query(HotelDB).filter(HotelDB.email == email.lower()).first()


def create_hotel(
    db: Session,
    *,
    name: str,
    email: str,
    password: str,
    location: str,
    description: str,
    accessibility_features: dict,
) -> HotelDB:
    """Create a hotel listing that can also log in as its own account."""
    hotel = HotelDB(
        id=str(uuid.uuid4()),
        name=name,
        email=email.lower(),
        password=password,
        location=location,
        description=description,
        rating=0,
        accessibility_features=accessibility_features,
    )
    db.add(hotel)
    db.commit()
    db.refresh(hotel)
    return hotel


def patch_hotel(db: Session, hotel_id: str, patch: dict) -> HotelDB | None:
    """Partially update editable hotel listing/account fields."""
    hotel = get_hotel_by_id(db, hotel_id)
    if hotel is None:
        return None

    if "name" in patch:
        hotel.name = patch["name"]
    if "email" in patch and patch["email"] is not None:
        hotel.email = patch["email"].lower()
    if "password" in patch and patch["password"] is not None:
        hotel.password = patch["password"]
    if "location" in patch:
        hotel.location = patch["location"]
    if "description" in patch:
        hotel.description = patch["description"]
    if "accessibility_features" in patch and patch["accessibility_features"] is not None:
        hotel.accessibility_features = patch["accessibility_features"]

    db.commit()
    db.refresh(hotel)
    return hotel
