from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator


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
    rating: int
    id: str


class CustomizedHotelDetails(BaseModel):
    name: str
    reviews: List[HotelReview]
    summary: List[str]


class HotelSummary(BaseModel):
    request_id: str
    reviews: List[HotelReview]
    summary: List[str]


class Hotel(BaseModel):
    city: str
    country: str
    name: str
    id: str
    num_reviews: Optional[int]

    @validator('num_reviews')
    def set_num_reviews(cls, v):
        if v is None:
            return 0
        else:
            return v


class UserRequest(BaseModel):
    user_id: str


class UserProfile(BaseModel):
    base_preferences: Dict[str, bool]
    additional_preferences: str
    travel_profile_summary: Optional[str]

    @validator('travel_profile_summary')
    def set_travel_profile_summary(cls, v):
        if v is None:
            return ""
        else:
            return v


class UserProfileSubmitRequest(BaseModel):
    user_id: str
    user_profile: UserProfile
