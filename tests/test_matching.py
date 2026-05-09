from app.data import HOTELS
from app.models import AccessibilityProfile, DietaryNeeds, MobilityNeeds, SearchRequest
from app.services import match_hotels


def test_exact_requested_features_return_full_match():
    profile = AccessibilityProfile(
        mobility=MobilityNeeds(wheelchair_accessible=True, ramp_access=True),
        dietary=DietaryNeeds(vegetarian=True),
    )

    results = match_hotels(HOTELS, "Paris", profile)

    hotel_access = results[0]
    assert hotel_access.hotel.name == "Hotel de l'Access"
    assert hotel_access.match_percentage == 100.0
    assert hotel_access.missing_needs == []


def test_partial_match_reports_missing_needs():
    profile = AccessibilityProfile(
        mobility=MobilityNeeds(wheelchair_accessible=True, accessible_bathroom=True),
        dietary=DietaryNeeds(vegetarian=True, halal=True),
    )

    results = match_hotels(HOTELS, "Paris", profile)
    voyageur = next(result for result in results if result.hotel.name == "Le Voyageur Hotel")

    assert voyageur.match_percentage == 50.0
    assert "mobility.accessible_bathroom" in voyageur.missing_needs
    assert "dietary.halal" in voyageur.missing_needs


def test_guest_search_request_does_not_require_user_account():
    request = SearchRequest(
        destination="Paris",
        accessibility_needs=AccessibilityProfile(
            mobility=MobilityNeeds(wheelchair_accessible=True)
        ),
    )

    results = match_hotels(HOTELS, request.destination, request.accessibility_needs)

    assert results
