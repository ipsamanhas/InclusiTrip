from __future__ import annotations

import json
import uuid
from pathlib import Path

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

HOTELS_JSON_PATH = Path(__file__).resolve().parent / "hotels.json"

USER_MAYA_ID = uuid.UUID("44444444-4444-4444-4444-444444444444")
USER_ALEX_ID = uuid.UUID("55555555-5555-5555-5555-555555555555")
USER_SAM_ID = uuid.UUID("66666666-6666-6666-6666-666666666666")
USER_PRIYA_ID = uuid.UUID("77777777-7777-7777-7777-777777777777")
OWNER_NORTHSTAR_ID = uuid.UUID("88888888-8888-8888-8888-888888888888")
OWNER_GLOBALSTAY_ID = uuid.UUID("99999999-9999-9999-9999-999999999999")
OWNER_CITYHAVEN_ID = uuid.UUID("aaaaaaaa-1111-1111-1111-aaaaaaaaaaaa")


def _hotel_id(index: int) -> uuid.UUID:
    return uuid.UUID(f"10000000-0000-0000-0000-{index:012d}")


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


HOTEL_OWNERS = [
    {
        "id": OWNER_NORTHSTAR_ID,
        "business_name": "Northstar Accessible Hospitality",
        "contact_name": "Jordan Lee",
        "email": "northstar-hotels@example.com",
        "password": "hotelpass123",
        "phone": "+1 604 555 0188",
    },
    {
        "id": OWNER_GLOBALSTAY_ID,
        "business_name": "GlobalStay Inclusive Group",
        "contact_name": "Amina Okafor",
        "email": "globalstay@example.com",
        "password": "globalstay123",
        "phone": "+44 20 5555 0199",
    },
    {
        "id": OWNER_CITYHAVEN_ID,
        "business_name": "CityHaven Hotels",
        "contact_name": "Mateo Silva",
        "email": "cityhaven@example.com",
        "password": "cityhaven123",
        "phone": "+1 212 555 0144",
    },
]


REVIEWS = [
    Review(
        id=uuid.UUID("20000000-0000-0000-0000-000000000001"),
        hotel_id=_hotel_id(1),
        rating=5,
        accessibility_category="mobility",
        comment="Wide hallways, ramps, and the accessible bathroom were all ready at check-in.",
    ),
    Review(
        id=uuid.UUID("20000000-0000-0000-0000-000000000002"),
        hotel_id=_hotel_id(2),
        rating=4,
        accessibility_category="sensory",
        comment="Quiet rooms were away from the elevators and the lighting was easy to adjust.",
    ),
    Review(
        id=uuid.UUID("20000000-0000-0000-0000-000000000003"),
        hotel_id=_hotel_id(4),
        rating=5,
        accessibility_category="speech",
        comment="Captions and multilingual support made front-desk communication simple.",
    ),
    Review(
        id=uuid.UUID("20000000-0000-0000-0000-000000000004"),
        hotel_id=_hotel_id(8),
        rating=4,
        accessibility_category="dietary",
        comment="The restaurant handled gluten-free and halal requests carefully.",
    ),
    Review(
        id=uuid.UUID("20000000-0000-0000-0000-000000000005"),
        hotel_id=_hotel_id(12),
        rating=5,
        accessibility_category="cognitive",
        comment="Clear signs and trained staff helped reduce travel stress.",
    ),
]


HOTELS = [
    Hotel(
        id=_hotel_id(1),
        name="Harbour Step-Free Suites",
        location="Vancouver, Canada",
        description="Waterfront hotel with strong mobility access and quiet upper-floor rooms.",
        rating=4.8,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                short_walking_distances=True,
                ramp_access=True,
                elevator_access=True,
                accessible_bathroom=True,
                wide_hallways=True,
            ),
            dietary=DietaryNeeds(vegetarian=True, vegan=True, gluten_free=True),
            speech=SpeechNeeds(captions=True, languages=["English", "French"]),
            sensory=SensoryNeeds(quiet_rooms=True, dimly_lit_spaces=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(2),
        name="Calm Quarter Hotel",
        location="Toronto, Canada",
        description="Downtown stay focused on sensory comfort, predictable layouts, and quiet rooms.",
        rating=4.6,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(elevator_access=True, short_walking_distances=True),
            dietary=DietaryNeeds(vegetarian=True, pescatarian=True, gluten_free=True),
            speech=SpeechNeeds(captions=True, languages=["English"]),
            sensory=SensoryNeeds(
                dimly_lit_spaces=True,
                quiet_rooms=True,
                sensory_rooms=True,
                weighted_blankets=True,
                aromatherapy_free_rooms=True,
            ),
            cognitive=CognitiveNeeds(clear_wayfinding=True, ibcces_certification=True),
        ),
    ),
    Hotel(
        id=_hotel_id(3),
        name="Cedar Ramp Lodge",
        location="Banff, Canada",
        description="Mountain lodge with ramps, elevators, and staff trained for mobility support.",
        rating=4.5,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                ramp_access=True,
                elevator_access=True,
                accessible_bathroom=True,
            ),
            dietary=DietaryNeeds(non_vegetarian=True, vegetarian=True),
            speech=SpeechNeeds(languages=["English"]),
            sensory=SensoryNeeds(quiet_rooms=True),
            cognitive=CognitiveNeeds(staff_disability_awareness_training=True),
        ),
    ),
    Hotel(
        id=_hotel_id(4),
        name="Canal Caption Inn",
        location="Amsterdam, Netherlands",
        description="Compact canal-side hotel with captions, multilingual staff, and step-free routing.",
        rating=4.4,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                ramp_access=True,
                elevator_access=True,
                wide_hallways=True,
            ),
            dietary=DietaryNeeds(vegetarian=True, vegan=True, kosher=True),
            speech=SpeechNeeds(
                hearing_impaired_support=True,
                speech_impaired_support=True,
                captions=True,
                languages=["Dutch", "English", "French"],
            ),
            sensory=SensoryNeeds(dimly_lit_spaces=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(5),
        name="Garden Allergy-Aware Stay",
        location="London, United Kingdom",
        description="Modern hotel with allergy-aware dining and flexible dietary accommodations.",
        rating=4.3,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(elevator_access=True, short_walking_distances=True),
            dietary=DietaryNeeds(
                vegetarian=True,
                vegan=True,
                gluten_free=True,
                halal=True,
                kosher=True,
                allergy_accommodations=["nuts", "dairy", "shellfish"],
            ),
            speech=SpeechNeeds(captions=True, languages=["English", "Arabic"]),
            sensory=SensoryNeeds(aromatherapy_free_rooms=True),
            cognitive=CognitiveNeeds(),
        ),
    ),
    Hotel(
        id=_hotel_id(6),
        name="Wayfinder Plaza",
        location="New York, United States",
        description="High-rise hotel with clear signs, trained staff, and accessible transit nearby.",
        rating=4.2,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                elevator_access=True,
                accessible_bathroom=True,
            ),
            dietary=DietaryNeeds(non_vegetarian=True, vegetarian=True, gluten_free=True),
            speech=SpeechNeeds(captions=True, languages=["English", "Spanish"]),
            sensory=SensoryNeeds(quiet_rooms=True),
            cognitive=CognitiveNeeds(
                clear_wayfinding=True,
                staff_disability_awareness_training=True,
            ),
        ),
    ),
    Hotel(
        id=_hotel_id(7),
        name="Lantern Quiet Rooms",
        location="Kyoto, Japan",
        description="Low-stimulation boutique hotel with quiet rooms and dim lighting options.",
        rating=4.7,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(elevator_access=True),
            dietary=DietaryNeeds(vegetarian=True, pescatarian=True),
            speech=SpeechNeeds(languages=["Japanese", "English"]),
            sensory=SensoryNeeds(
                dimly_lit_spaces=True,
                quiet_rooms=True,
                weighted_blankets=True,
                fidget_tools=True,
            ),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(8),
        name="Atlas Inclusive Hotel",
        location="Marrakesh, Morocco",
        description="Full-service hotel with halal dining, accessible bathrooms, and multilingual staff.",
        rating=4.5,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                ramp_access=True,
                accessible_bathroom=True,
                wide_hallways=True,
            ),
            dietary=DietaryNeeds(halal=True, vegetarian=True, vegan=True, gluten_free=True),
            speech=SpeechNeeds(languages=["Arabic", "English", "French"]),
            sensory=SensoryNeeds(quiet_rooms=True, aromatherapy_free_rooms=True),
            cognitive=CognitiveNeeds(staff_disability_awareness_training=True),
        ),
    ),
    Hotel(
        id=_hotel_id(9),
        name="Beacon Sign Support Hotel",
        location="Berlin, Germany",
        description="Urban hotel with sign-language support, captions, and strong transit access.",
        rating=4.4,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                elevator_access=True,
                short_walking_distances=True,
            ),
            dietary=DietaryNeeds(vegetarian=True, vegan=True),
            speech=SpeechNeeds(
                hearing_impaired_support=True,
                sign_language=True,
                captions=True,
                languages=["German", "English"],
            ),
            sensory=SensoryNeeds(),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(10),
        name="Seabreeze Accessible Resort",
        location="Barcelona, Spain",
        description="Beach resort with ramps, wide routes, accessible bathrooms, and diet-friendly meals.",
        rating=4.6,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                ramp_access=True,
                elevator_access=True,
                accessible_bathroom=True,
                wide_hallways=True,
            ),
            dietary=DietaryNeeds(
                non_vegetarian=True,
                pescatarian=True,
                vegetarian=True,
                gluten_free=True,
            ),
            speech=SpeechNeeds(captions=True, languages=["Spanish", "English"]),
            sensory=SensoryNeeds(quiet_rooms=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(11),
        name="Remote Comfort Suites",
        location="Singapore",
        description="Tech-forward hotel with remote-controlled room features and accessible circulation.",
        rating=4.8,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                remote_controlled_doors=True,
                remote_controlled_curtains=True,
                remote_controlled_lights=True,
                elevator_access=True,
                accessible_bathroom=True,
            ),
            dietary=DietaryNeeds(vegetarian=True, vegan=True, halal=True),
            speech=SpeechNeeds(captions=True, languages=["English", "Mandarin", "Malay"]),
            sensory=SensoryNeeds(dimly_lit_spaces=True, quiet_rooms=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(12),
        name="Neurodiverse Welcome Hotel",
        location="Orlando, United States",
        description="Family-focused hotel with sensory rooms, clear wayfinding, and trained staff.",
        rating=4.7,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                short_walking_distances=True,
                elevator_access=True,
            ),
            dietary=DietaryNeeds(vegetarian=True, gluten_free=True),
            speech=SpeechNeeds(captions=True, languages=["English", "Spanish"]),
            sensory=SensoryNeeds(
                sensory_rooms=True,
                noise_cancelling_support=True,
                weighted_blankets=True,
                fidget_tools=True,
                aromatherapy_free_rooms=True,
            ),
            cognitive=CognitiveNeeds(
                ibcces_certification=True,
                clear_wayfinding=True,
                staff_disability_awareness_training=True,
            ),
        ),
    ),
    Hotel(
        id=_hotel_id(13),
        name="Old Town Lift Hotel",
        location="Prague, Czech Republic",
        description="Historic hotel retrofitted with elevators, ramps, and accessible bathrooms.",
        rating=4.1,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                ramp_access=True,
                elevator_access=True,
                accessible_bathroom=True,
            ),
            dietary=DietaryNeeds(non_vegetarian=True, vegetarian=True),
            speech=SpeechNeeds(languages=["Czech", "English"]),
            sensory=SensoryNeeds(dimly_lit_spaces=True),
            cognitive=CognitiveNeeds(),
        ),
    ),
    Hotel(
        id=_hotel_id(14),
        name="Riverfront Gluten-Free Inn",
        location="Portland, United States",
        description="Independent inn known for gluten-free breakfast and quiet accessible rooms.",
        rating=4.3,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                ramp_access=True,
                accessible_bathroom=True,
            ),
            dietary=DietaryNeeds(
                vegetarian=True,
                vegan=True,
                gluten_free=True,
                allergy_accommodations=["gluten", "nuts"],
            ),
            speech=SpeechNeeds(captions=True, languages=["English"]),
            sensory=SensoryNeeds(quiet_rooms=True, aromatherapy_free_rooms=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(15),
        name="Skyline Easy-Way Hotel",
        location="Sydney, Australia",
        description="Central hotel with step-free access, wide hallways, and multilingual services.",
        rating=4.5,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                short_walking_distances=True,
                ramp_access=True,
                elevator_access=True,
                wide_hallways=True,
            ),
            dietary=DietaryNeeds(pescatarian=True, vegetarian=True, vegan=True),
            speech=SpeechNeeds(captions=True, languages=["English", "Mandarin"]),
            sensory=SensoryNeeds(quiet_rooms=True),
            cognitive=CognitiveNeeds(
                clear_wayfinding=True,
                staff_disability_awareness_training=True,
            ),
        ),
    ),
    Hotel(
        id=_hotel_id(16),
        name="Pacific Quiet Access Hotel",
        location="Vancouver, Canada",
        description="Central hotel with quiet rooms, elevator access, and gluten-free dining.",
        rating=4.4,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                elevator_access=True,
                accessible_bathroom=True,
            ),
            dietary=DietaryNeeds(vegetarian=True, gluten_free=True),
            speech=SpeechNeeds(captions=True, languages=["English"]),
            sensory=SensoryNeeds(quiet_rooms=True, weighted_blankets=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(17),
        name="False Creek Comfort Inn",
        location="Vancouver, Canada",
        description="Accessible waterfront inn with ramps, short walking routes, and vegan breakfast.",
        rating=4.2,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                short_walking_distances=True,
                ramp_access=True,
                wide_hallways=True,
            ),
            dietary=DietaryNeeds(vegetarian=True, vegan=True),
            speech=SpeechNeeds(languages=["English", "Mandarin"]),
            sensory=SensoryNeeds(dimly_lit_spaces=True),
            cognitive=CognitiveNeeds(staff_disability_awareness_training=True),
        ),
    ),
    Hotel(
        id=_hotel_id(28),
        name="Budget City Rooms Vancouver",
        location="Vancouver, Canada",
        description="Basic downtown rooms with standard amenities and no confirmed accessibility accommodations.",
        rating=3.6,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(),
            dietary=DietaryNeeds(non_vegetarian=True),
            speech=SpeechNeeds(languages=["English"]),
            sensory=SensoryNeeds(),
            cognitive=CognitiveNeeds(),
        ),
    ),
    Hotel(
        id=_hotel_id(18),
        name="Toronto Caption Suites",
        location="Toronto, Canada",
        description="Accessible downtown suites with captions, elevators, and allergy-aware meals.",
        rating=4.5,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                elevator_access=True,
                accessible_bathroom=True,
            ),
            dietary=DietaryNeeds(
                vegetarian=True,
                vegan=True,
                gluten_free=True,
                allergy_accommodations=["nuts", "dairy"],
            ),
            speech=SpeechNeeds(
                hearing_impaired_support=True,
                captions=True,
                languages=["English", "French"],
            ),
            sensory=SensoryNeeds(quiet_rooms=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(19),
        name="Distillery District Lift Hotel",
        location="Toronto, Canada",
        description="Boutique hotel with elevator access, calm public spaces, and pescatarian dining.",
        rating=4.1,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(elevator_access=True, short_walking_distances=True),
            dietary=DietaryNeeds(pescatarian=True, vegetarian=True, halal=True),
            speech=SpeechNeeds(languages=["English"]),
            sensory=SensoryNeeds(dimly_lit_spaces=True, aromatherapy_free_rooms=True),
            cognitive=CognitiveNeeds(),
        ),
    ),
    Hotel(
        id=_hotel_id(20),
        name="Midtown Step-Free Hotel",
        location="New York, United States",
        description="Step-free Midtown hotel with ramps, elevators, captions, and vegetarian dining.",
        rating=4.6,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                ramp_access=True,
                elevator_access=True,
                accessible_bathroom=True,
                wide_hallways=True,
            ),
            dietary=DietaryNeeds(vegetarian=True, vegan=True, kosher=True),
            speech=SpeechNeeds(captions=True, languages=["English", "Spanish"]),
            sensory=SensoryNeeds(quiet_rooms=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(21),
        name="Brooklyn Sensory Stay",
        location="New York, United States",
        description="Low-stimulation hotel with sensory supports and trained accessibility staff.",
        rating=4.3,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(elevator_access=True, short_walking_distances=True),
            dietary=DietaryNeeds(vegetarian=True, gluten_free=True),
            speech=SpeechNeeds(captions=True, languages=["English"]),
            sensory=SensoryNeeds(
                sensory_rooms=True,
                noise_cancelling_support=True,
                weighted_blankets=True,
                fidget_tools=True,
            ),
            cognitive=CognitiveNeeds(
                clear_wayfinding=True,
                staff_disability_awareness_training=True,
            ),
        ),
    ),
    Hotel(
        id=_hotel_id(22),
        name="Thames Accessible House",
        location="London, United Kingdom",
        description="Riverside hotel with accessible bathrooms, lifts, and multilingual support.",
        rating=4.5,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                ramp_access=True,
                elevator_access=True,
                accessible_bathroom=True,
            ),
            dietary=DietaryNeeds(vegetarian=True, vegan=True, halal=True, gluten_free=True),
            speech=SpeechNeeds(captions=True, languages=["English", "French"]),
            sensory=SensoryNeeds(quiet_rooms=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(23),
        name="Covent Garden Calm Rooms",
        location="London, United Kingdom",
        description="Quiet central hotel with aromatherapy-free rooms and clear wayfinding.",
        rating=4.2,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(elevator_access=True),
            dietary=DietaryNeeds(vegetarian=True, gluten_free=True, kosher=True),
            speech=SpeechNeeds(languages=["English"]),
            sensory=SensoryNeeds(
                dimly_lit_spaces=True,
                quiet_rooms=True,
                aromatherapy_free_rooms=True,
            ),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(24),
        name="Marina Bay Universal Suites",
        location="Singapore",
        description="Luxury suites with remote-controlled room features and halal-friendly dining.",
        rating=4.7,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                remote_controlled_doors=True,
                remote_controlled_curtains=True,
                remote_controlled_lights=True,
                elevator_access=True,
                accessible_bathroom=True,
            ),
            dietary=DietaryNeeds(vegetarian=True, vegan=True, halal=True, gluten_free=True),
            speech=SpeechNeeds(captions=True, languages=["English", "Mandarin", "Malay"]),
            sensory=SensoryNeeds(quiet_rooms=True, dimly_lit_spaces=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(25),
        name="Sentosa Sensory Resort",
        location="Singapore",
        description="Resort with sensory rooms, noise-cancelling support, and step-free routes.",
        rating=4.4,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                short_walking_distances=True,
                ramp_access=True,
                elevator_access=True,
            ),
            dietary=DietaryNeeds(pescatarian=True, vegetarian=True, halal=True),
            speech=SpeechNeeds(languages=["English", "Mandarin"]),
            sensory=SensoryNeeds(
                sensory_rooms=True,
                noise_cancelling_support=True,
                weighted_blankets=True,
                aromatherapy_free_rooms=True,
            ),
            cognitive=CognitiveNeeds(staff_disability_awareness_training=True),
        ),
    ),
    Hotel(
        id=_hotel_id(26),
        name="Lake Buena Vista Accessible Inn",
        location="Orlando, United States",
        description="Family-friendly accessible inn with short walking routes and allergy-aware menus.",
        rating=4.4,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(
                wheelchair_accessible=True,
                short_walking_distances=True,
                ramp_access=True,
                accessible_bathroom=True,
            ),
            dietary=DietaryNeeds(
                vegetarian=True,
                vegan=True,
                gluten_free=True,
                allergy_accommodations=["nuts", "dairy"],
            ),
            speech=SpeechNeeds(captions=True, languages=["English", "Spanish"]),
            sensory=SensoryNeeds(quiet_rooms=True, fidget_tools=True),
            cognitive=CognitiveNeeds(clear_wayfinding=True),
        ),
    ),
    Hotel(
        id=_hotel_id(27),
        name="Sunshine Sensory Suites",
        location="Orlando, United States",
        description="Resort-style hotel with sensory rooms, weighted blankets, and trained staff.",
        rating=4.6,
        accessibility_features=HotelAccessibilityFeatures(
            mobility=MobilityNeeds(elevator_access=True, short_walking_distances=True),
            dietary=DietaryNeeds(vegetarian=True, halal=True),
            speech=SpeechNeeds(captions=True, languages=["English"]),
            sensory=SensoryNeeds(
                sensory_rooms=True,
                noise_cancelling_support=True,
                weighted_blankets=True,
                aromatherapy_free_rooms=True,
            ),
            cognitive=CognitiveNeeds(
                ibcces_certification=True,
                clear_wayfinding=True,
                staff_disability_awareness_training=True,
            ),
        ),
    ),
]

for hotel in HOTELS:
    hotel.reviews = [review for review in REVIEWS if review.hotel_id == hotel.id]


DEFAULT_GUEST_PROFILE = AccessibilityProfile()


def _seed_owner_id_for_hotel(index: int) -> str:
    owner_ids = [OWNER_NORTHSTAR_ID, OWNER_GLOBALSTAY_ID, OWNER_CITYHAVEN_ID]
    return str(owner_ids[index % len(owner_ids)])


def _load_hotels_from_json(db, json_path: Path = HOTELS_JSON_PATH) -> int:
    """Upsert hotels from a JSON file into the database.

    Skips entries whose `id` already exists, or whose `name` + `location`
    pair already exists in the table.

    Returns the number of newly inserted hotels.
    """
    from app.models.db_models import HotelDB

    if not json_path.exists():
        return 0

    with json_path.open("r", encoding="utf-8") as fp:
        payload = json.load(fp)

    raw_hotels = payload.get("hotels") if isinstance(payload, dict) else payload
    if not isinstance(raw_hotels, list):
        return 0

    existing_ids = {hid for (hid,) in db.query(HotelDB.id).all()}
    existing_pairs = {
        (name.strip().lower(), loc.strip().lower())
        for (name, loc) in db.query(HotelDB.name, HotelDB.location).all()
        if name and loc
    }

    inserted = 0
    for index, raw in enumerate(raw_hotels):
        hotel_id = str(raw.get("id") or uuid.uuid4())
        name = str(raw.get("name", "")).strip()
        location = str(raw.get("location", "")).strip()

        if not name or not location:
            continue
        if hotel_id in existing_ids:
            continue
        pair_key = (name.lower(), location.lower())
        if pair_key in existing_pairs:
            continue

        features_raw = raw.get("accessibility_features") or {}
        features = HotelAccessibilityFeatures.model_validate(features_raw)

        owner_id = raw.get("owner_id") or _seed_owner_id_for_hotel(index)

        db.add(
            HotelDB(
                id=hotel_id,
                owner_id=owner_id,
                name=name,
                location=location,
                description=str(raw.get("description", "")).strip(),
                rating=float(raw.get("rating", 0.0)),
                accessibility_features=features.model_dump(),
            )
        )
        existing_ids.add(hotel_id)
        existing_pairs.add(pair_key)
        inserted += 1

    return inserted


def seed_database() -> None:
    """Insert seed users, hotels, and reviews into empty database tables."""
    from app.database import SessionLocal
    from app.models.db_models import HotelDB, HotelOwnerDB, ReviewDB, UserDB

    db = SessionLocal()
    try:
        if db.query(UserDB).first() is None:
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

        if db.query(HotelOwnerDB).first() is None:
            for owner in HOTEL_OWNERS:
                db_owner = HotelOwnerDB(
                    id=str(owner["id"]),
                    business_name=str(owner["business_name"]),
                    contact_name=str(owner["contact_name"]),
                    email=str(owner["email"]).lower(),
                    password=str(owner["password"]),
                    phone=str(owner["phone"]),
                )
                db.add(db_owner)

        existing_hotel_ids = {
            hotel_id for (hotel_id,) in db.query(HotelDB.id).all()
        }
        if len(existing_hotel_ids) < len(HOTELS):
            for index, hotel in enumerate(HOTELS):
                if str(hotel.id) in existing_hotel_ids:
                    continue
                db_hotel = HotelDB(
                    id=str(hotel.id),
                    owner_id=_seed_owner_id_for_hotel(index),
                    name=hotel.name,
                    location=hotel.location,
                    description=hotel.description,
                    rating=hotel.rating,
                    accessibility_features=hotel.accessibility_features.model_dump(),
                )
                db.add(db_hotel)

        # Owner FKs need to exist before we flush hotel rows that reference them.
        db.flush()

        _load_hotels_from_json(db)

        for index, hotel in enumerate(db.query(HotelDB).order_by(HotelDB.name).all()):
            if hotel.owner_id is None:
                hotel.owner_id = _seed_owner_id_for_hotel(index)

        if db.query(ReviewDB).first() is None:
            for review in REVIEWS:
                db_review = ReviewDB(
                    id=str(review.id),
                    user_id=str(review.user_id) if review.user_id else None,
                    hotel_id=str(review.hotel_id),
                    rating=review.rating,
                    accessibility_category=review.accessibility_category,
                    comment=review.comment,
                )
                db.add(db_review)

        db.commit()
    finally:
        db.close()
