from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from app.database import get_db
from app.data.hotels import list_hotels
from app.data.searches import create_user_search
from app.models.models import (
    SearchRequest,
    SearchResponse,
    AccessibilityProfile,
    MobilityNeeds,
    DietaryNeeds,
    SpeechNeeds,
    SensoryNeeds,
    CognitiveNeeds,
)
from app.services import match_hotels

router = APIRouter(tags=["search"])


def parse_query_params_to_accessibility_profile(query_params: dict) -> AccessibilityProfile:
    """Convert query parameters to AccessibilityProfile object.
    
    Query params use dot notation: mobility.wheelchair_accessible=true, dietary.vegetarian=true, etc.
    """
    mobility_data = {}
    dietary_data = {}
    speech_data = {}
    sensory_data = {}
    cognitive_data = {}
    
    for key, value in query_params.items():
        if key.startswith("mobility."):
            field = key.replace("mobility.", "")
            if field == "allergy_accommodations":
                mobility_data[field] = value.split(",") if isinstance(value, str) else value
            else:
                mobility_data[field] = value.lower() in ("true", "1", "yes")
        elif key.startswith("dietary."):
            field = key.replace("dietary.", "")
            if field == "allergy_accommodations":
                dietary_data[field] = value.split(",") if isinstance(value, str) else value
            else:
                dietary_data[field] = value.lower() in ("true", "1", "yes")
        elif key.startswith("speech."):
            field = key.replace("speech.", "")
            if field == "languages":
                speech_data[field] = value.split(",") if isinstance(value, str) else value
            else:
                speech_data[field] = value.lower() in ("true", "1", "yes")
        elif key.startswith("sensory."):
            field = key.replace("sensory.", "")
            sensory_data[field] = value.lower() in ("true", "1", "yes")
        elif key.startswith("cognitive."):
            field = key.replace("cognitive.", "")
            cognitive_data[field] = value.lower() in ("true", "1", "yes")
    
    return AccessibilityProfile(
        mobility=MobilityNeeds(**mobility_data) if mobility_data else MobilityNeeds(),
        dietary=DietaryNeeds(**dietary_data) if dietary_data else DietaryNeeds(),
        speech=SpeechNeeds(**speech_data) if speech_data else SpeechNeeds(),
        sensory=SensoryNeeds(**sensory_data) if sensory_data else SensoryNeeds(),
        cognitive=CognitiveNeeds(**cognitive_data) if cognitive_data else CognitiveNeeds(),
    )


@router.get("/api/search", response_model=SearchResponse)
def search_hotels_get(
    request: Request,
    destination: str = Query(...),
    user_id: Optional[str] = Query(None),
    guests: int = Query(1, ge=1),
    db: Session = Depends(get_db),
) -> SearchResponse:
    """Match hotels for a destination and accessibility profile via GET with query parameters.
    
    Usage: GET /api/search?destination=Toronto&mobility.wheelchair_accessible=true&dietary.vegetarian=true
    """
    # Parse accessibility needs from all query parameters
    accessibility_needs = parse_query_params_to_accessibility_profile(
        dict(request.query_params)
    )
    
    results = match_hotels(
        hotels=list_hotels(db),
        destination=destination,
        accessibility_needs=accessibility_needs,
    )
    
    # Create a SearchRequest for the response
    search_request = SearchRequest(
        destination=destination,
        user_id=uuid.UUID(user_id) if user_id else None,
        accessibility_needs=accessibility_needs,
        guests=guests,
    )
    
    stored_search = create_user_search(db, search_request)
    
    return SearchResponse(
        search_id=stored_search.id if stored_search is not None else None,
        search=search_request,
        results=results,
    )


@router.post("/api/search", response_model=SearchResponse)
def search_hotels_post(
    request: SearchRequest,
    db: Session = Depends(get_db),
) -> SearchResponse:
    """Match hotels for a destination and accessibility profile via POST with JSON body."""
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
