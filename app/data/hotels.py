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
