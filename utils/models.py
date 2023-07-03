from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str


class Answer(BaseModel):
    question: str
    answer: str
