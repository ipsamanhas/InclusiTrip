from __future__ import annotations

from typing import Any, Iterable, List, Tuple

from pydantic import BaseModel

from app.models import AccessibilityProfile, Hotel, HotelMatchResult


def match_hotels(
    hotels: Iterable[Hotel],
    destination: str,
    accessibility_needs: AccessibilityProfile,
) -> List[HotelMatchResult]:
    destination_normalized = destination.strip().lower()
    matching_location_hotels = [
        hotel for hotel in hotels if destination_normalized in hotel.location.lower()
    ]

    results = [
        _build_match_result(hotel, accessibility_needs)
        for hotel in matching_location_hotels
    ]
    return sorted(
        results,
        key=lambda result: (
            result.match_percentage,
            result.hotel.rating,
        ),
        reverse=True,
    )


def _build_match_result(
    hotel: Hotel,
    accessibility_needs: AccessibilityProfile,
) -> HotelMatchResult:
    requested_needs = _requested_need_paths(accessibility_needs)
    if not requested_needs:
        return HotelMatchResult(
            hotel=hotel,
            match_percentage=100.0,
            matched_needs=[],
            missing_needs=[],
        )

    matched_needs: List[str] = []
    missing_needs: List[str] = []

    for need_path, requested_value in requested_needs:
        hotel_value = _get_nested_value(hotel.accessibility_features, need_path)
        if _feature_matches(requested_value, hotel_value):
            matched_needs.append(need_path)
        else:
            missing_needs.append(need_path)

    match_percentage = round((len(matched_needs) / len(requested_needs)) * 100, 1)
    return HotelMatchResult(
        hotel=hotel,
        match_percentage=match_percentage,
        matched_needs=matched_needs,
        missing_needs=missing_needs,
    )


def _requested_need_paths(model: BaseModel, prefix: str = "") -> List[Tuple[str, Any]]:
    requested: List[Tuple[str, Any]] = []
    for field_name, value in model:
        path = f"{prefix}.{field_name}" if prefix else field_name
        if isinstance(value, BaseModel):
            requested.extend(_requested_need_paths(value, path))
        elif isinstance(value, list):
            if value:
                requested.append((path, value))
        elif value is True:
            requested.append((path, value))
    return requested


def _get_nested_value(model: BaseModel, path: str) -> Any:
    value: Any = model
    for part in path.split("."):
        value = getattr(value, part)
    return value


def _feature_matches(requested_value: Any, hotel_value: Any) -> bool:
    if isinstance(requested_value, list):
        requested_items = {str(item).strip().lower() for item in requested_value}
        hotel_items = {str(item).strip().lower() for item in hotel_value}
        return requested_items.issubset(hotel_items)
    return hotel_value is True
