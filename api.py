from typing import Dict, List, Union

from fastapi import FastAPI, BackgroundTasks

from utils.localCORS import permitReactLocalhostClient
from utils.ai import enable_llm_cache
from utils.db import get_keyspace, get_session
from utils.models import (
    CustomizedHotelDetails,
    Hotel,
    HotelDetailsRequest,
    HotelReview,
    HotelSearchRequest,
    HotelSummary,
    UserRequest,
    UserProfileSubmitRequest,
    UserProfile,
)

from utils.review_llm import summarize_reviews_for_hotel, summarize_reviews_for_user
from utils.reviews import (
    select_general_hotel_reviews,
    insert_review_for_hotel,
    select_hotel_reviews_for_user,
)
from utils.users import (
    read_user_profile,
    write_user_profile,
    update_user_travel_profile_summary,
)
from utils.hotels import find_hotels_by_location, find_hotel_by_id

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


# Endpoint that retrieves the travel preferences (base + additional prefs) of the specified user.
# This has been implemented (TODO remove this note)
# TODO should this just be a GET, e.g. /v1/user_profile/{user_id} ?
@app.post("/v1/get_user_profile")
def get_user_profile(payload: UserRequest) -> Union[UserProfile, None]:
    return read_user_profile(payload.user_id)


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


# Endpoint that inserts a review for a hotel.
# This has been implemented (TODO remove this note)
@app.post("/v1/{hotel_id}/add_review")
def add_review(hotel_id: str, payload: HotelReview):
    insert_review_for_hotel(
        hotel_id=hotel_id,
        review_title=payload.title,
        review_body=payload.body,
        review_rating=payload.rating,
    )


# Endpoint that selects the three reviews of this hotel that are most relevant to this user
# and generates a user-tailored summary of these reviews.
# This has been implemented (TODO remove this note)
# TODO should this become a GET and have the user_id as part of the path somewhere?
@app.post("/v1/customized_hotel_details/{hotel_id}")
def get_customized_hotel_details(
    hotel_id: str, payload: UserRequest
) -> CustomizedHotelDetails:
    """
    1. retrieve user data (esp. textual description)
    2. retrieve *user-relevant* reviews with ANN search
    3. retrieve hotel details
    4. stuff 1 and 2 into a prompt "get me a short summary"
    5. call the LLM to get the short summary (which takes advantage of the auto cache prompt->response)
    6. return the summary and the reviews used (+ name), as in the structure below
    """

    user_profile = read_user_profile(payload.user_id)

    hotel_reviews_for_user = select_hotel_reviews_for_user(
        hotel_id=hotel_id,
        user_travel_profile_summary=user_profile.travel_profile_summary,
    )

    customized_review_summary = summarize_reviews_for_user(reviews=hotel_reviews_for_user, travel_profile_summary=user_profile.travel_profile_summary)
    hotel_details = find_hotel_by_id(hotel_id)

    return CustomizedHotelDetails(
        name=hotel_details.name,
        summary=customized_review_summary,
        reviews=hotel_reviews_for_user,
    )
