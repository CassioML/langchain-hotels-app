from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class ReviewRequest(BaseModel):
    review: str


class Answer(BaseModel):
    question: str
    answer: str


class HotelSearchWithReviewsRequest(BaseModel):
    hotel_city: str
    hotel_country: str
    trip_preferences: str


class HotelSearchWithReviewsAnswer(BaseModel):
    hotel_name: str
    hotel_city: str
    hotel_country: str
    hotel_reviews: list[str]

