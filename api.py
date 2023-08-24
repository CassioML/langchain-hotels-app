from typing import Any, Dict, List, Union

from fastapi import FastAPI, BackgroundTasks, Depends

from utils.localCORS import permitReactLocalhostClient
from utils.ai import get_embeddings, enable_llm_cache
from utils.db import get_keyspace, get_session
from utils.dbio import find_hotels_by_country_city
from utils.models import (
    CustomizedHotelDetails,
    Hotel,
    HotelDetailsRequest,
    HotelReview,
    HotelSearchRequest,
    HotelSummary,
    ReviewRequest,
    UserRequest,
    UserProfileSubmitRequest,
    UserProfile,
)
from utils.review_vectors import find_similar_reviews, get_review_vectorstore
from utils.review_llm import summarize_review_list
from utils.users import read_user_preferences, write_user_profile, update_user_desc

db_session = get_session()
db_keyspace = get_keyspace()


def fa_review_store():
    emb = get_embeddings()
    yield get_review_vectorstore(
        session=db_session, keyspace=db_keyspace, embeddings=emb
    )


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

#
# @app.get("/")
# def index():
#     return {"data": "Here it is."}
#
#
# @app.get("/capitalize/{input}")
# def cap(input):
#     return {"data": capitalize(input)}


# TODO: handle per-hotel search
# TODO: replace with 'summarize reviews found' (etc)
@app.post("/find_reviews")
def find_reviews(
    review_request: ReviewRequest, review_store=Depends(fa_review_store)
) -> List[str]:
    similar_reviews = find_similar_reviews(review_request.review, review_store)
    return similar_reviews


# TEMPORARY - not hotel-specific
@app.post("/summarize_reviews")
def summarize_reviews(
    review_request: ReviewRequest, review_store=Depends(fa_review_store)
) -> Dict[str, Union[str, List[str]]]:
    similar_reviews = find_similar_reviews(review_request.review, review_store)
    fake_user_preferences = (
        "Travels with kids. Highly values amenities. Hates having to walk."
    )
    summary = summarize_review_list(similar_reviews, fake_user_preferences)
    return {
        "reviews": similar_reviews,
        "summary": summary,
    }


# Searches hotels by city and country.
@app.post("/find_hotels")
def find_hotels(hotel_request: HotelSearchRequest) -> List[Hotel]:
    hotels = find_hotels_by_country_city(
        db_session, db_keyspace, **hotel_request.dict()
    )
    return hotels


## MOCKS FOR CLIENT DEVELOPMENT.
## the plan: these will become the real endpoints, all others would be scrubbed.


@app.post("/v1/get_user_profile")
def get_user_profile(payload: UserRequest) -> UserProfile:
    return read_user_preferences(payload.user_id)


@app.post("/v1/set_user_profile")
def set_user_profile(
    payload: UserProfileSubmitRequest, bg_tasks: BackgroundTasks
) -> Dict[str, bool]:
    # TODO replace the hardcoded additional prefs with the input coming from the front-end
    try:
        write_user_profile(
            payload.user_id,
            payload.profileData,
            "I love ice skating and ice-cream parlours",
        )
        bg_tasks.add_task(
            update_user_desc,
            user_id=payload.user_id,
            base_preferences=payload.profileData,
            additional_preferences="I love ice skating and ice-cream parlours",
        )
        return {
            "success": True,
        }
    except Exception:
        return {
            "success": False,
        }


@app.post("/v1/find_hotels")
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


@app.post("/v1/base_hotel_summary")
def get_base_hotel_summary(payload: HotelDetailsRequest) -> HotelSummary:
    import time

    time.sleep(1.5)
    print(
        f"asked SUMMARY [{payload.request_id}] for {payload.country}/{payload.city}/{payload.id}"
    )
    return HotelSummary(
        request_id=payload.request_id,
        summary=f"A fake summary for hotel #{payload.id}",
    )


@app.post("/v1/customized_hotel_details/{hotel_id}")
def get_customized_hotel_details(
    hotel_id: str, payload: UserRequest
) -> CustomizedHotelDetails:
    """
    TODO:
    1. retrieve user data (esp. textual description)
    2. retrieve *user-relevant* reviews with ANN search
    3. stuff 1 and 2 into a prompt "get me a short summary"
    4. call the LLM to get the short summary (which takes advantage of the auto cache prompt->response)
    5. return the summary and the reviews used (+ name), as in the structure below
    """
    import time

    time.sleep(0.8)
    return CustomizedHotelDetails(
        name=f"Hotel Name {hotel_id}",
        summary=f"Fake AI-generated summary for hotel {hotel_id} and user {payload.user_id}",
        reviews=[
            HotelReview(
                id=f"r_{hotel_id}_{i}",
                title=f"Review #{i}",
                body=f"This is review #{i} for hotel with id={hotel_id}. Nice view on a dumpster.",
            )
            for i in range(3)
        ],
    )
