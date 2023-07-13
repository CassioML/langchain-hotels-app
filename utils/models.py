from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class ReviewRequest(BaseModel):
    review: str

class Answer(BaseModel):
    question: str
    answer: str
