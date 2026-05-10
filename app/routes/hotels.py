from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data.hotels import (
    create_hotel,
    db_hotel_to_model,
    get_hotel_by_email,
    get_hotel_by_id,
    patch_hotel,
)
from app.data.users import hash_password, verify_password
from app.database import get_db
from app.models.db_models import HotelDB
from app.models.models import Hotel, HotelLoginRequest, HotelSignupRequest, HotelUpdateRequest

router = APIRouter(tags=["hotels"])


def hotel_to_response(hotel: HotelDB) -> Hotel:
    return db_hotel_to_model(hotel)


@router.post(
    "/api/hotels/signup",
    response_model=Hotel,
    status_code=status.HTTP_201_CREATED,
)
def handle_hotel_signup(
    request: HotelSignupRequest,
    db: Session = Depends(get_db),
) -> Hotel:
    existing_hotel = get_hotel_by_email(db, request.email)
    if existing_hotel is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A hotel account with this email already exists.",
        )

    hotel = create_hotel(
        db=db,
        name=request.name,
        email=request.email,
        password=hash_password(request.password),
        location=request.location,
        description=request.description,
        accessibility_features=request.accessibility_features.model_dump(),
    )
    return hotel_to_response(hotel)


@router.post("/api/hotels/login")
def handle_hotel_login(
    credentials: HotelLoginRequest,
    db: Session = Depends(get_db),
):
    hotel = get_hotel_by_email(db, credentials.email)
    if hotel is None or not hotel.password or not verify_password(credentials.password, hotel.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="We could not find a hotel account with those login details.",
        )

    return {
        "authenticated": True,
        "hotel_id": hotel.id,
        "name": hotel.name,
    }


@router.get(
    "/api/hotels/{hotel_id}",
    response_model=Hotel,
)
def get_hotel_profile(
    hotel_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Hotel:
    hotel = get_hotel_by_id(db, str(hotel_id))
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found.")
    return hotel_to_response(hotel)


@router.patch(
    "/api/hotels/{hotel_id}",
    response_model=Hotel,
)
def update_hotel_profile(
    hotel_id: uuid.UUID,
    request: HotelUpdateRequest,
    db: Session = Depends(get_db),
) -> Hotel:
    payload = request.model_dump(exclude_unset=True)

    if "email" in payload and payload["email"] is not None:
        existing = get_hotel_by_email(db, payload["email"])
        if existing is not None and str(existing.id) != str(hotel_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A hotel account with this email already exists.",
            )

    if "password" in payload and payload["password"] is not None:
        payload["password"] = hash_password(payload["password"])

    if "accessibility_features" in payload and payload["accessibility_features"] is not None:
        features = payload["accessibility_features"]
        payload["accessibility_features"] = (
            features.model_dump() if hasattr(features, "model_dump") else features
        )

    updated = patch_hotel(db, str(hotel_id), payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found.")

    return hotel_to_response(updated)
