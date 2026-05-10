from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.data.users import create_user, get_user_by_email, verify_password
from app.models.models import CreateAccountRequest, LoginRequest, UserResponse
from app.routes.users import user_to_response

router = APIRouter(tags=["auth"])


@router.post("/api/login")
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, credentials.email)
    if user is None or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "We could not find an account with those login details. "
                "Please create an account or continue as a guest."
            ),
        )

    return {
        "authenticated": True,
        "user_id": user.id,
        "profile_url": f"/api/users/{user.id}/profile",
    }


@router.post(
    "/api/create-account",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def handle_create_account(
    request: CreateAccountRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
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

    return user_to_response(new_user)
