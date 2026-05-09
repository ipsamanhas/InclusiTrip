from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.data.users import create_user, get_user_by_email
from app.models import CreateAccountRequest, UserResponse

router = APIRouter(tags=["auth"])


@router.post(
    "/api/create-account",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def handle_create_account(
    request: CreateAccountRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    """Create a new user account and store it in the database."""
    existing_user = get_user_by_email(db, request.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    new_user = create_user(
        db=db,
        name=request.name,
        email=request.email,
        password=request.password,
    )

    return UserResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        accessibility_profile=None,
    )
