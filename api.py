from typing import Any, Dict, List, Union

from fastapi import FastAPI, BackgroundTasks, Depends

from utils.localCORS import permitReactLocalhostClient
from utils.ai import get_embeddings, enable_llm_cache
from utils.db import get_keyspace, get_session
from utils.dbio import find_hotels_by_country_city
from utils.models import HotelSearchRequest, Hotel, ReviewRequest, UserProfileRequest, UserProfileSubmitRequest
from utils.review_vectors import find_similar_reviews, get_review_vectorstore
from utils.review_llm import summarize_review_list
from utils.users import read_user_profile, write_user_profile, update_user_desc

UserProfile = Dict[str, Any]

db_session = get_session()
db_keyspace = get_keyspace()

def fa_review_store():
    emb = get_embeddings()
    yield get_review_vectorstore(session=db_session, keyspace=db_keyspace, embeddings=emb)


# init

def init():
    enable_llm_cache(
        get_session(),
        get_keyspace(),
    )


# app

init()
app = FastAPI()
permitReactLocalhostClient(app)

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
def summarize_reviews(review_request: ReviewRequest, review_store=Depends(fa_review_store)) -> Dict[str, Union[str, List[str]]]:
    similar_reviews = find_similar_reviews(review_request.review, review_store)
    fake_user_preferences = "Travels with kids. Highly values amenities. Hates having to walk."
    summary = summarize_review_list(similar_reviews, fake_user_preferences)
    return {
        "reviews": similar_reviews,
        "summary": summary,
    }


# Searches hotels by city and country.
@app.post('/find_hotels')
def find_hotels(hotel_request: HotelSearchRequest) -> List[Hotel]:
    hotels = find_hotels_by_country_city(db_session, db_keyspace, **hotel_request.dict())
    return hotels


## MOCKS FOR CLIENT DEVELOPMENT.
## the plan: these will become the real endpoints, all others would be scrubbed.


@app.post('/v1/get_user_profile')
def get_user_profile(payload: UserProfileRequest) -> UserProfile:
    return read_user_profile(payload.user_id)


@app.post('/v1/set_user_profile')
def get_user_profile(payload: UserProfileSubmitRequest, bg_tasks: BackgroundTasks) -> Dict[str, str]:
    try:
        write_user_profile(payload.user_id, payload.profileData)
        bg_tasks.add_task(update_user_desc, user_id=payload.user_id, profile=payload.profileData)
        return {
            "success": True,
        }
    except Exception:
        return {
            "success": False,
        }


@app.post('/v1/find_hotels')
def get_hotels(hotel_request: HotelSearchRequest) -> List[Hotel]:
    import time
    time.sleep(1)
    return [
        Hotel(
            city="hotel_city",
            country="hotel_country",
            name="hotel_name_0",
            id="hotel_id_0",
        ),
        Hotel(
            city="hotel_city",
            country="hotel_country",
            name="hotel_name_1",
            id="hotel_id_1",
        ),
    ]
