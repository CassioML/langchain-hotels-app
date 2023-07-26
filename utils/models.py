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
