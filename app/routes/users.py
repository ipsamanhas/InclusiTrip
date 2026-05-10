from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.data.users import (
    get_user_by_email,
    get_user_by_id,
    patch_user_profile,
    update_user_profile,
)
from app.models.db_models import UserDB
from app.models.models import AccessibilityProfile, UpdateAccountRequest, UserResponse

router = APIRouter(tags=["users"])


def user_to_response(user: UserDB) -> UserResponse:
    profile: AccessibilityProfile | None = None
    if user.accessibility_profile is not None:
        profile = AccessibilityProfile.model_validate(user.accessibility_profile)

    uid = user.id if isinstance(user.id, uuid.UUID) else uuid.UUID(str(user.id))
    return UserResponse(
        id=uid,
        name=user.name,
        email=user.email,
        phone=user.phone,
        photo_url=user.photo_url,
        accessibility_profile=profile,
    )


@router.get(
    "/api/users/{user_id}/profile",
    response_model=UserResponse,
)
def get_user_profile(
    user_id: str,
    db: Session = Depends(get_db),
) -> UserResponse:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found.")

    return user_to_response(user)


@router.get(
    "/api/users/{user_id}/accessibility-preferences",
    response_model=AccessibilityProfile,
)
def get_user_accessibility_preferences(
    user_id: str,
    db: Session = Depends(get_db),
) -> AccessibilityProfile:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found.")

    if user.accessibility_profile is None:
        return AccessibilityProfile()

    return AccessibilityProfile.model_validate(user.accessibility_profile)


@router.put(
    "/api/users/{user_id}/profile",
    response_model=UserResponse,
)
def handle_update_profile(
    user_id: str,
    profile: AccessibilityProfile,
    db: Session = Depends(get_db),
) -> UserResponse:
    updated_user = update_user_profile(
        db=db,
        user_id=user_id,
        accessibility_profile=profile.model_dump(),
    )

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user_to_response(updated_user)


@router.patch(
    "/api/users/{user_id}",
    response_model=UserResponse,
)
def handle_update_account(
    user_id: str,
    request: UpdateAccountRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    payload = request.model_dump(exclude_unset=True)

    if "email" in payload and payload["email"] is not None:
        existing = get_user_by_email(db, payload["email"])
        if existing is not None and str(existing.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

    if not payload:
        user = get_user_by_id(db, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return user_to_response(user)

    updated_user = patch_user_profile(db=db, user_id=user_id, patch=payload)

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user_to_response(updated_user)
