from __future__ import annotations

import uuid

from app.models import (
    AccessibilityProfile,
    CognitiveNeeds,
    DietaryNeeds,
    Hotel,
    HotelAccessibilityFeatures,
    MobilityNeeds,
    Review,
    SensoryNeeds,
    SpeechNeeds,
)

HOTEL_ACCESS_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
HOTEL_COMFORT_ID = uuid.UUID("22222222-2222-2222-2222-222222222222")
HOTEL_VOYAGEUR_ID = uuid.UUID("33333333-3333-3333-3333-333333333333")


REVIEWS = [
    Review(
        id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1"),
        hotel_id=HOTEL_ACCESS_ID,
        rating=5,
        accessibility_category="mobility",
        comment="The step-free entrance and accessible bathroom made the stay much easier.",
    ),
    Review(
        id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa2"),
        hotel_id=HOTEL_ACCESS_ID,
        rating=5,
        accessibility_category="speech",
        comment="The front desk had sign language support and captions were already enabled.",
    ),
    Review(
        id=uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb1"),
        hotel_id=HOTEL_COMFORT_ID,
        rating=4,
        accessibility_category="dietary",
        comment="Staff were confident with gluten-free breakfast and checked ingredients twice.",
    ),
    Review(
        id=uuid.UUID("cccccccc-cccc-cccc-cccc-ccccccccccc1"),
        hotel_id=HOTEL_VOYAGEUR_ID,
        rating=3,
        accessibility_category="mobility",
        comment="The elevator helped, but the bathroom setup was tight for wheelchair users.",
    ),
]


HOTELS = [
    Hotel(
        id=HOTEL_ACCESS_ID,
        name="Hotel de l'Access",
        location="Paris, France",
        description="Central hotel with strong mobility support and trained accessibility staff.",
        rating=4.7,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                short_walking_distances=True,
                ramp_access=True,
                elevator_access=True,
                accessible_bathroom=True,
                wide_hallways=True,
            ),
            dietary=DietaryNeeds(
                vegetarian=True,
                vegan=True,
                gluten_free=True,
                allergy_accommodations=["nuts", "gluten", "dairy"],
            ),
            speech=SpeechNeeds(
                hearing_impaired_support=True,
                sign_language=True,
                captions=True,
                languages=["English", "French"],
            ),
            sensory=SensoryNeeds(dimly_lit_spaces=True, quiet_rooms=True),
            cognitive=CognitiveNeeds(
                clear_wayfinding=True,
                staff_disability_awareness_training=True,
            ),
        ),
        reviews=[review for review in REVIEWS if review.hotel_id == HOTEL_ACCESS_ID],
    ),
    Hotel(
        id=HOTEL_COMFORT_ID,
        name="Comfort Stay Paris",
        location="Paris, France",
        description="Calm boutique stay with accessible rooms and strong dietary accommodations.",
        rating=4.4,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                ramp_access=True,
                elevator_access=True,
                accessible_bathroom=True,
            ),
            dietary=DietaryNeeds(
                vegetarian=True,
                pescatarian=True,
                gluten_free=True,
                allergy_accommodations=["nuts", "gluten"],
            ),
            speech=SpeechNeeds(captions=True, languages=["English", "French", "Spanish"]),
            sensory=SensoryNeeds(quiet_rooms=True, weighted_blankets=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
        reviews=[review for review in REVIEWS if review.hotel_id == HOTEL_COMFORT_ID],
    ),
    Hotel(
        id=HOTEL_VOYAGEUR_ID,
        name="Le Voyageur Hotel",
        location="Paris, France",
        description="Affordable hotel with basic accessibility features near transit.",
        rating=4.1,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                elevator_access=True,
                short_walking_distances=True,
            ),
            dietary=DietaryNeeds(vegetarian=True, non_vegetarian=True),
            speech=SpeechNeeds(languages=["French"]),
            sensory=SensoryNeeds(dimly_lit_spaces=True),
            cognitive=CognitiveNeeds(),
        ),
        reviews=[review for review in REVIEWS if review.hotel_id == HOTEL_VOYAGEUR_ID],
    ),
]


DEFAULT_GUEST_PROFILE = AccessibilityProfile()
