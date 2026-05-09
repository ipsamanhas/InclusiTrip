from __future__ import annotations

import hashlib
import secrets
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.db_models import UserDB


def hash_password(plain_password: str) -> str:
    """Hash a password with a random salt using SHA-256."""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}{plain_password}".encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(plain_password: str, stored_password: str) -> bool:
    """Verify a plain password against the stored salt:hash string."""
    if ":" not in stored_password:
        return plain_password == stored_password
    salt, hashed = stored_password.split(":")
    return hashlib.sha256(f"{salt}{plain_password}".encode()).hexdigest() == hashed


def get_user_by_email(db: Session, email: str) -> Optional[UserDB]:
    """Look up a user by their email address."""
    return db.query(UserDB).filter(UserDB.email == email.lower()).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[UserDB]:
    """Look up a user by their UUID."""
    return db.query(UserDB).filter(UserDB.id == user_id).first()


def create_user(
    db: Session,
    name: str,
    email: str,
    password: str,
    accessibility_profile: Optional[dict] = None,
) -> UserDB:
    """Create a new user and save to the database."""
    hashed_pw = hash_password(password)
    new_user = UserDB(
        id=str(uuid.uuid4()),
        name=name,
        email=email.lower(),
        password=hashed_pw,
        accessibility_profile=accessibility_profile,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
