"""Utilities to manipulate reviews"""
import random
import uuid, datetime
import cassio

from common_constants import FEATURED_VOTE_THRESHOLD, REVIEWS_TABLE_NAME
from utils.models import HotelReview

from utils.ai import get_embeddings, EMBEDDING_DIMENSION
from utils.db import get_session, get_keyspace
from utils.review_vectors import REVIEW_VECTOR_TABLE_NAME, get_review_vectorstore
from utils.hotels import find_hotel_by_id

from typing import List, Dict

select_recent_reviews_stmt = None
select_featured_reviews_stmt = None
insert_review_stmt = None

# ### SELECTING REVIEWS


# Entry point to select reviews for the general (base) hotel summary
def select_general_hotel_reviews(hotel_id) -> List[HotelReview]:
    session = get_session()
    keyspace = get_keyspace()

    review_dict = {}

    global select_recent_reviews_stmt
    if select_recent_reviews_stmt is None:
        select_recent_reviews_stmt = session.prepare(
            f"SELECT id, title, body, rating FROM {keyspace}.{REVIEWS_TABLE_NAME} WHERE hotel_id = ? LIMIT 3"
        )

    rows_recent = session.execute(select_recent_reviews_stmt, (hotel_id,))
    for row in rows_recent:
        review_dict[row.id] = HotelReview(id=row.id, title=row.title, body=row.body, rating=row.rating)

    global select_featured_reviews_stmt
    if select_featured_reviews_stmt is None:
        select_featured_reviews_stmt = session.prepare(
            f"SELECT id, title, body, rating FROM {keyspace}.{REVIEWS_TABLE_NAME} WHERE hotel_id = ? and featured = 1 LIMIT 3"
        )

    rows_featured = session.execute(select_recent_reviews_stmt, (hotel_id,))
    for row in rows_featured:
        review_dict[row.id] = HotelReview(id=row.id, title=row.title, body=row.body, rating=row.rating)

    return list(review_dict.values())

# TODO add function to retrieve reviews relevant to a user


# ### ADDING REVIEWS

# Entry point for when we want to add a review
# - Generates an id for the new review
# - Stores the review in the non-vectorised table
# - Embeds the review and then stores it in the vectorised table
def insert_review_for_hotel(
    hotel_id: str, review_title: str, review_body: str, review_rating: int
):
    review_id = generate_review_id()
    insert_into_reviews_table(hotel_id, review_id, review_title, review_body, review_rating)

    db_session = get_session()
    db_keyspace = get_keyspace()
    embeddings = get_embeddings()

    review_store = get_review_vectorstore(
        session=db_session,
        keyspace=db_keyspace,
        embeddings=embeddings,
    )    

    review_metadata = {
        "hotel_id": hotel_id,
        "rating": review_rating,
    }

    review_store.add_texts(
        texts=[format_review_content_for_embedding(review_title, review_body)],
        metadatas=[review_metadata],
        ids=[review_id],
        partition_id=hotel_id,
    )


def generate_review_id():
    return uuid.uuid4().hex


def format_review_content_for_embedding(title: str, body: str) -> str:
    return f"{title}: {body}"


def choose_featured(num_upvotes: int) -> int:
    if num_upvotes > FEATURED_VOTE_THRESHOLD:
        return 1
    else:
        return 0


def insert_into_reviews_table(
    hotel_id: str, review_id: str, review_title: str, review_body: str, review_rating: int
):
    session = get_session()
    keyspace = get_keyspace()

    global insert_review_stmt
    if insert_review_stmt is None:
        insert_review_stmt = session.prepare(
            f"""INSERT INTO {keyspace}.{REVIEWS_TABLE_NAME} (hotel_id, date_added, id, title, body, rating, featured) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)"""
        )

    date_added = datetime.datetime.now()
    featured = choose_featured(random.randint(1, 21))

    session.execute(
        insert_review_stmt,
        (hotel_id, date_added, review_id, review_title, review_body, review_rating, featured),
    )
