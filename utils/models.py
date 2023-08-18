from typing import Dict

from pydantic import BaseModel


class ReviewRequest(BaseModel):
    review: str


class HotelSearchRequest(BaseModel):
    city: str
    country: str


class Hotel(BaseModel):
    city: str
    country: str
    name: str
    id: str


class UserProfileRequest(BaseModel):
    user_id: str

class UserProfileSubmitRequest(BaseModel):
    user_id: str
    profileData: Dict[str, bool]
