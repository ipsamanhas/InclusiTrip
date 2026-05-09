from __future__ import annotations

import hashlib
import secrets
from typing import Dict, Optional

from app.models import User


USERS_DB: Dict[str, User] = {}


def hash_password(plain_password: str) -> str:
    """Hash a password with a random salt using SHA-256."""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}{plain_password}".encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(plain_password: str, stored_password: str) -> bool:
    """Verify a plain password against the stored salt:hash string."""
    salt, hashed = stored_password.split(":")
    return hashlib.sha256(f"{salt}{plain_password}".encode()).hexdigest() == hashed


def get_user_by_email(email: str) -> Optional[User]:
    """Look up a user by their email address."""
    return USERS_DB.get(email.lower())


def save_user(user: User) -> None:
    """Save a user to the store, keyed by lowercase email."""
    USERS_DB[user.email.lower()] = user
