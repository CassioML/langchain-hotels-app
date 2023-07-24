from typing import List

from fastapi import FastAPI, Depends

from utils.ai import capitalize, get_embeddings, get_answer, enable_llm_cache
from utils.db import get_keyspace, get_session
from utils.models import QuestionRequest, Answer, ReviewRequest
from utils.review_vectors import find_similar_reviews, get_review_vectorstore
from utils.review_llm import summarize_review_list


# helpers
def fa_session():
    yield get_session()


def fa_ks():
    yield get_keyspace()


def fa_review_store():
    emb = get_embeddings()
    session = get_session()
    ks = get_keyspace()
    yield get_review_vectorstore(session=session, keyspace=ks, embeddings=emb)


# init

def init():
    enable_llm_cache(
        get_session(),
        get_keyspace(),
    )


# app

init()
app = FastAPI()


@app.get('/')
def index():
    return {'data': 'Here it is.'}


@app.get('/capitalize/{input}')
def cap(input):
    return {'data': capitalize(input)}


@app.get('/people/{n}')
def people(n: int, session=Depends(fa_session), ks=Depends(fa_ks)):
    rows = session.execute(f'SELECT * FROM {ks}.people LIMIT %s', (n, ))

    returned = [
        {
            'city': row.city,
            'name': row.name,
        }
        for row in rows
    ]

    return {'data': returned}


@app.post('/qa')
def qa(question_request: QuestionRequest) -> Answer:
    answer = get_answer(question_request.question)
    return Answer(
        question=question_request.question,
        answer=answer,
    )


# TODO: handle per-hotel search
# TODO: replace with 'summarize reviews found' (etc)
@app.post('/find_reviews')
def find_reviews(review_request: ReviewRequest, review_store=Depends(fa_review_store)) -> List[str]:
    similar_reviews = find_similar_reviews(review_request.review, review_store)
    return similar_reviews


# TEMPORARY - not hotel-specific
@app.post('/summarize_reviews')
def summarize_reviews(review_request: ReviewRequest, review_store=Depends(fa_review_store)) -> str:
    similar_reviews = find_similar_reviews(review_request.review, review_store)
    fake_user_preferences = "Travels with kids. Highly values amenities. Hates having to walk."
    return summarize_review_list(similar_reviews, fake_user_preferences)

# Searches hotels by city and country. For each hotel, finds reviews relevant to the user's trip preferences.
# @app.post('/find_hotels')
# def find_hotels(hotel_request: HotelSearchWithReviewsRequest,
# review_store=Depends(fa_review_store)) -> List[HotelSearchWithReviewsAnswer]:
#     hotels = find_hotels_by_location(hotel_request.hotel_city, hotel_request.hotel_country)
#
#     for hotel in hotels:



