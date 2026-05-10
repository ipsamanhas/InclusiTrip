from __future__ import annotations
import uuid
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class MobilityNeeds(BaseModel):
    wheelchair_accessible: bool = False
    short_walking_distances: bool = False
    long_walking_distances: bool = False
    remote_controlled_doors: bool = False
    remote_controlled_curtains: bool = False
    remote_controlled_lights: bool = False
    ramp_access: bool = False
    elevator_access: bool = False
    accessible_bathroom: bool = False
    wide_hallways: bool = False


class DietaryNeeds(BaseModel):
    non_vegetarian: bool = False
    pescatarian: bool = False
    vegetarian: bool = False
    vegan: bool = False
    gluten_free: bool = False
    halal: bool = False
    kosher: bool = False
    allergy_accommodations: List[str] = Field(default_factory=list)


class SpeechNeeds(BaseModel):
    hearing_impaired_support: bool = False
    speech_impaired_support: bool = False
    sign_language: bool = False
    captions: bool = False
    languages: List[str] = Field(default_factory=list)


class SensoryNeeds(BaseModel):
    dimly_lit_spaces: bool = False
    quiet_rooms: bool = False
    sensory_rooms: bool = False
    noise_cancelling_support: bool = False
    weighted_blankets: bool = False
    fidget_tools: bool = False
    aromatherapy_free_rooms: bool = False


class CognitiveNeeds(BaseModel):
    ibcces_certification: bool = False
    clear_wayfinding: bool = False
    staff_disability_awareness_training: bool = False


class AccessibilityProfile(BaseModel):
    mobility: MobilityNeeds = Field(default_factory=MobilityNeeds)
    dietary: DietaryNeeds = Field(default_factory=DietaryNeeds)
    speech: SpeechNeeds = Field(default_factory=SpeechNeeds)
    sensory: SensoryNeeds = Field(default_factory=SensoryNeeds)
    cognitive: CognitiveNeeds = Field(default_factory=CognitiveNeeds)


class HotelAccessibilityFeatures(BaseModel):
    mobility: MobilityNeeds = Field(default_factory=MobilityNeeds)
    dietary: DietaryNeeds = Field(default_factory=DietaryNeeds)
    speech: SpeechNeeds = Field(default_factory=SpeechNeeds)
    sensory: SensoryNeeds = Field(default_factory=SensoryNeeds)
    cognitive: CognitiveNeeds = Field(default_factory=CognitiveNeeds)


class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    email: EmailStr
    password: str
    accessibility_profile: Optional[AccessibilityProfile] = None


class Review(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: Optional[uuid.UUID] = None
    hotel_id: uuid.UUID
    rating: int = Field(ge=1, le=5)
    accessibility_category: str
    comment: str


class Hotel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    location: str
    description: str
    rating: float = Field(ge=0, le=5)
    accessibility_features: HotelAccessibilityFeatures
    reviews: List[Review] = Field(default_factory=list)


class CreateAccountRequest(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=8)


class UpdateAccountRequest(BaseModel):
    """Partial update payload for a user's editable account fields."""
    name: Optional[str] = Field(default=None, min_length=1)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=64)
    photo_url: Optional[str] = Field(default=None, max_length=1_300_000)
    accessibility_profile: Optional[AccessibilityProfile] = None


class UserResponse(BaseModel):
    """Safe user representation that excludes the password."""
    id: uuid.UUID
    name: str
    email: EmailStr
    phone: Optional[str] = None
    photo_url: Optional[str] = None
    accessibility_profile: Optional[AccessibilityProfile] = None


class SearchRequest(BaseModel):
    destination: str
    user_id: Optional[uuid.UUID] = None
    accessibility_needs: AccessibilityProfile = Field(default_factory=AccessibilityProfile)
    guests: int = Field(default=1, ge=1)


class HotelMatchResult(BaseModel):
    hotel: Hotel
    match_percentage: float
    matched_needs: List[str]
    missing_needs: List[str]


class SearchResponse(BaseModel):
    search_id: Optional[uuid.UUID] = None
    search: SearchRequest
    results: List[HotelMatchResult]
