from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.db_models import SearchDB
from app.models.models import SearchRequest


def create_user_search(db: Session, request: SearchRequest) -> Optional[SearchDB]:
    """Persist a search only when it belongs to a logged-in user."""
    if request.user_id is None:
        return None

    search = SearchDB(
        id=str(uuid.uuid4()),
        user_id=str(request.user_id),
        destination=request.destination,
        guests=request.guests,
        accessibility_needs=request.accessibility_needs.model_dump(),
    )
    db.add(search)
    db.commit()
    db.refresh(search)
    return search
