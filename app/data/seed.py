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
    User,
)

HOTEL_ACCESS_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
HOTEL_COMFORT_ID = uuid.UUID("22222222-2222-2222-2222-222222222222")
HOTEL_VOYAGEUR_ID = uuid.UUID("33333333-3333-3333-3333-333333333333")
USER_MAYA_ID = uuid.UUID("44444444-4444-4444-4444-444444444444")
USER_ALEX_ID = uuid.UUID("55555555-5555-5555-5555-555555555555")
USER_SAM_ID = uuid.UUID("66666666-6666-6666-6666-666666666666")
USER_PRIYA_ID = uuid.UUID("77777777-7777-7777-7777-777777777777")


USERS = [
    User(
        id=USER_MAYA_ID,
        name="Maya Chen",
        email="maya@example.com",
        password="password123",
        accessibility_profile=AccessibilityProfile(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                ramp_access=True,
                elevator_access=True,
                accessible_bathroom=True,
            ),
            dietary=DietaryNeeds(vegetarian=True, gluten_free=True),
            speech=SpeechNeeds(captions=True, languages=["English", "French"]),
            sensory=SensoryNeeds(quiet_rooms=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    User(
        id=USER_ALEX_ID,
        name="Alex Rivera",
        email="alex@example.com",
        password="travel2026",
        accessibility_profile=AccessibilityProfile(
            mobility=MobilityNeeds(short_walking_distances=True, elevator_access=True),
            dietary=DietaryNeeds(vegan=True, allergy_accommodations=["nuts"]),
            speech=SpeechNeeds(languages=["English", "Spanish"]),
            sensory=SensoryNeeds(dimly_lit_spaces=True, quiet_rooms=True),
        ),
    ),
    User(
        id=USER_SAM_ID,
        name="Sam Patel",
        email="sam@example.com",
        password="guestpass",
        accessibility_profile=AccessibilityProfile(
            dietary=DietaryNeeds(halal=True, gluten_free=True),
            speech=SpeechNeeds(
                hearing_impaired_support=True,
                sign_language=True,
                captions=True,
            ),
            cognitive=CognitiveNeeds(staff_disability_awareness_training=True),
        ),
    ),
    User(
        id=USER_PRIYA_ID,
        name="Priya Nair",
        email="priya@example.com",
        password="inclusive",
        accessibility_profile=AccessibilityProfile(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                wide_hallways=True,
                remote_controlled_doors=True,
            ),
            sensory=SensoryNeeds(
                sensory_rooms=True,
                noise_cancelling_support=True,
                aromatherapy_free_rooms=True,
            ),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
]


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


def seed_database() -> None:
    """Insert seed users into the database if the users table is empty."""
    from app.database import SessionLocal
    from app.models.db_models import UserDB

    db = SessionLocal()
    try:
        if db.query(UserDB).first() is not None:
            return

        for user in USERS:
            db_user = UserDB(
                id=str(user.id),
                name=user.name,
                email=user.email.lower(),
                password=user.password,
                accessibility_profile=(
                    user.accessibility_profile.model_dump()
                    if user.accessibility_profile
                    else None
                ),
            )
            db.add(db_user)

        db.commit()
    finally:
        db.close()
