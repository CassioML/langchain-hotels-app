from typing import Dict, List, Any

from pydantic import BaseModel


class ReviewRequest(BaseModel):
    review: str


class HotelSearchRequest(BaseModel):
    city: str
    country: str


class HotelDetailsRequest(BaseModel):
    request_id: str
    city: str
    country: str
    id: str


class HotelReview(BaseModel):
    title: str
    body: str
    id: str


class CustomizedHotelDetails(BaseModel):
    name: str
    reviews: List[HotelReview]
    summary: str


class HotelSummary(BaseModel):
    request_id: str
    reviews: List[HotelReview]
    summary: str


class Hotel(BaseModel):
    city: str
    country: str
    name: str
    id: str


class UserRequest(BaseModel):
    user_id: str


class UserProfile(BaseModel):
    base_preferences: Dict[str, bool]
    additional_preferences: str


class UserProfileSubmitRequest(BaseModel):
    user_id: str
    user_profile: UserProfile
