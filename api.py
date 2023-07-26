from typing import List

from fastapi import FastAPI, Depends

from utils.ai import get_embeddings, enable_llm_cache
from utils.db import get_keyspace, get_session
from utils.dbio import find_hotels_by_country_city
from utils.models import HotelSearchRequest, Hotel, ReviewRequest
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

# Searches hotels by city and country.
@app.post('/find_hotels')
def find_hotels(hotel_request: HotelSearchRequest, session=Depends(fa_session), ks=Depends(fa_ks)) -> List[Hotel]:
    hotels = find_hotels_by_country_city(session, ks, **hotel_request.dict())
    return hotels
