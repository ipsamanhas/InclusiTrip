from app.data import HOTELS
from app.models import AccessibilityProfile, DietaryNeeds, MobilityNeeds, SearchRequest
from app.services import match_hotels


def test_exact_requested_features_return_full_match():
    profile = AccessibilityProfile(
        mobility=MobilityNeeds(wheelchair_accessible=True, ramp_access=True),
        dietary=DietaryNeeds(vegan=True),
    )

    results = match_hotels(HOTELS, "Vancouver", profile)

    harbour = results[0]
    assert harbour.hotel.name == "Harbour Step-Free Suites"
    assert harbour.match_percentage == 100.0
    assert harbour.missing_needs == []


def test_partial_match_reports_missing_needs():
    profile = AccessibilityProfile(
        mobility=MobilityNeeds(wheelchair_accessible=True, accessible_bathroom=True),
        dietary=DietaryNeeds(vegetarian=True, halal=True),
    )

    results = match_hotels(HOTELS, "New York", profile)
    wayfinder = next(result for result in results if result.hotel.name == "Wayfinder Plaza")

    assert wayfinder.match_percentage == 75.0
    assert "dietary.halal" in wayfinder.missing_needs


def test_guest_search_request_does_not_require_user_account():
    request = SearchRequest(
        destination="Toronto",
        accessibility_needs=AccessibilityProfile(
            mobility=MobilityNeeds(wheelchair_accessible=True)
        ),
    )

    results = match_hotels(HOTELS, request.destination, request.accessibility_needs)

    assert results
