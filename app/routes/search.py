from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.data.hotels import list_hotels
from app.data.searches import create_user_search
from app.models.models import SearchRequest, SearchResponse
from app.services import match_hotels

router = APIRouter(tags=["search"])


@router.post("/api/search", response_model=SearchResponse)
def search_hotels(
    request: SearchRequest,
    db: Session = Depends(get_db),
) -> SearchResponse:
    """Match hotels for a destination and accessibility profile."""
    results = match_hotels(
        hotels=list_hotels(db),
        destination=request.destination,
        accessibility_needs=request.accessibility_needs,
    )
    stored_search = create_user_search(db, request)
    return SearchResponse(
        search_id=stored_search.id if stored_search is not None else None,
        search=request,
        results=results,
    )
