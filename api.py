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
from utils.review_llm import summarize_reviews_for_user, summarize_reviews_for_hotel
from utils.reviews import select_general_hotel_reviews, insert_review_for_hotel
from utils.users import (
    read_user_preferences,
    write_user_profile,
    update_user_travel_profile_summary,
)
from utils.hotels import find_hotels_by_location

db_session = get_session()
db_keyspace = get_keyspace()


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


# TODO: handle per-hotel search
# TODO: replace with 'summarize reviews found' (etc)
@app.post("/find_reviews")
def find_reviews(review_request: ReviewRequest) -> List[str]:
    hotel_id = "AVwdp-5bIN2L1WUfx-QW"
    print("FIXME, I AM A FAKE HOTEL ID")
    review_store = get_review_vectorstore(
        session=db_session,
        keyspace=db_keyspace,
        embeddings=get_embeddings(),
    )
    similar_reviews = find_similar_reviews(
        review_request.review, hotel_id, review_store
    )
    return similar_reviews


# TODO - change to be hotel-specific
@app.post("/summarize_reviews")
def summarize_reviews(
    review_request: ReviewRequest,
) -> Dict[str, Union[str, List[str]]]:
    hotel_id = "AVwdp-5bIN2L1WUfx-QW"
    print("FIXME, I AM A FAKE HOTEL ID")
    review_store = get_review_vectorstore(
        session=db_session,
        keyspace=db_keyspace,
        embeddings=get_embeddings(),
    )
    similar_reviews = find_similar_reviews(
        review_request.review, hotel_id, review_store
    )
    fake_user_preferences = (
        "Travels with kids. Highly values amenities. Hates having to walk."
    )
    summary = summarize_reviews_for_user(similar_reviews, fake_user_preferences)
    return {
        "reviews": similar_reviews,
        "summary": summary,
    }


@app.post("/find_hotels")
def find_hotels(hotel_request: HotelSearchRequest) -> List[Hotel]:
    hotels = find_hotels_by_country_city(
        db_session, db_keyspace, **hotel_request.dict()
    )
    return hotels


## MOCKS FOR CLIENT DEVELOPMENT.
## the plan: these will become the real endpoints, all others would be scrubbed.


# Endpoint that retrieves the travel preferences (base + additional prefs) of the specified user.
# This has been implemented (TODO remove this note)
@app.post("/v1/get_user_profile")
def get_user_profile(payload: UserRequest) -> Union[UserProfile, None]:
    return read_user_preferences(payload.user_id)


# Endpoint that stores the travel preferences (base + additional prefs) of the specified user.
# It also calls the LLM to create the travel profile summary, and stores the summary in the user's profile.
# This has been implemented (TODO remove this note)
@app.post("/v1/set_user_profile")
def set_user_profile(
    payload: UserProfileSubmitRequest, bg_tasks: BackgroundTasks
) -> Dict[str, bool]:
    try:
        write_user_profile(
            payload.user_id,
            payload.user_profile,
        )
        bg_tasks.add_task(
            update_user_travel_profile_summary,
            user_id=payload.user_id,
            user_profile=payload.user_profile,
        )
        return {
            "success": True,
        }
    except Exception:
        return {
            "success": False,
        }


# Endpoint that retrieves a list of hotels located in the specified city.
# This has been implemented (TODO remove this note)
# TODO implement geo search based on proximity to a point
@app.post("/v1/find_hotels")
def get_hotels(hotel_request: HotelSearchRequest) -> List[Hotel]:
    return find_hotels_by_location(hotel_request.city, hotel_request.country)


# Endpoint that selects the most recent reviews + some featured ones and creates a general concise summary.
# This has been implemented (TODO remove this note)
@app.post("/v1/base_hotel_summary")
def get_base_hotel_summary(payload: HotelDetailsRequest) -> HotelSummary:
    hotel_reviews = select_general_hotel_reviews(payload.id)
    hotel_review_summary = summarize_reviews_for_hotel(hotel_reviews)
    return HotelSummary(
        request_id=payload.request_id,
        reviews=hotel_reviews,
        summary=hotel_review_summary,
    )


# TODO review / improve the path of this endpoint
@app.post("/v1/{hotel_id}/add_review")
def add_review(hotel_id: str, payload: HotelReview):
    insert_review_for_hotel(hotel_id=hotel_id, review_title=payload.title, review_body=payload.body)


# TODO should this become a GET and have the user_id as part of the path somewhere?
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
