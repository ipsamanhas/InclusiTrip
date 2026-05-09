from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.data.users import get_user_by_email, hash_password, save_user
from app.models import CreateAccountRequest, User, UserResponse

router = APIRouter(tags=["auth"])


@router.post(
    "/create-account",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def handle_create_account(request: CreateAccountRequest) -> UserResponse:
    """Create a new user account and store it in the database."""
    existing_user = get_user_by_email(request.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    hashed_pw = hash_password(request.password)

    new_user = User(
        name=request.name,
        email=request.email,
        password=hashed_pw,
    )
    save_user(new_user)

    return UserResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        accessibility_profile=new_user.accessibility_profile,
    )
