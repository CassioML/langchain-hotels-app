"""Utilities to manipulate reviews"""
import random
import uuid, datetime

from common_constants import FEATURED_VOTE_THRESHOLD, REVIEWS_TABLE_NAME
from utils.models import HotelReview

from utils.db import get_session, get_keyspace

from typing import List

select_recent_reviews_stmt = None
select_featured_reviews_stmt = None
insert_review_stmt = None


def generate_review_id():
    return uuid.uuid4().hex


def review_for_embeddings(title: str, body: str) -> str:
    return f"{title}: {body}"


def choose_featured(num_upvotes: int) -> int:
    if num_upvotes > FEATURED_VOTE_THRESHOLD:
        return 1
    else:
        return 0


def insert_into_reviews_table(hotel_id: str, review_id: str, review_title: str, review_body: str):
    session = get_session()
    keyspace = get_keyspace()

    global insert_review_stmt
    if insert_review_stmt is None:
        insert_review_stmt = session.prepare(
            f"""INSERT INTO {keyspace}.{REVIEWS_TABLE_NAME} (hotel_id, date_added, id, title, body, featured) 
                    VALUES (?, ?, ?, ?, ?, ?)"""
        )

    date_added = datetime.datetime.now()
    featured = choose_featured(random.randint(1, 21))

    session.execute(insert_review_stmt, (hotel_id, date_added, review_id, review_title, review_body, featured))

# TODO impelment
# def insert_into_reviews_vector_table(hotel_id: str, review_id: str, review_title: str, review_body: str):
#

def insert_review_for_hotel(hotel_id: str, review_title: str, review_body: str):
    review_id = generate_review_id()
    insert_into_reviews_table(hotel_id, review_id, review_title, review_body)





def select_general_hotel_reviews(hotel_id) -> List[HotelReview]:
    session = get_session()
    keyspace = get_keyspace()

    review_dict = {}

    global select_recent_reviews_stmt
    if select_recent_reviews_stmt is None:
        select_recent_reviews_stmt = session.prepare(
            f"SELECT id, title, body FROM {keyspace}.{REVIEWS_TABLE_NAME} WHERE hotel_id = ? LIMIT 3"
        )

    rows_recent = session.execute(select_recent_reviews_stmt, (hotel_id,))
    for row in rows_recent:
        review_dict[row.id] = HotelReview(id=row.id, title=row.title, body=row.body)

    global select_featured_reviews_stmt
    if select_featured_reviews_stmt is None:
        select_featured_reviews_stmt = session.prepare(
            f"SELECT id, title, body FROM {keyspace}.{REVIEWS_TABLE_NAME} WHERE hotel_id = ? and featured = 1 LIMIT 3"
        )

    rows_featured = session.execute(select_recent_reviews_stmt, (hotel_id,))
    for row in rows_featured:
        review_dict[row.id] = HotelReview(id=row.id, title=row.title, body=row.body)

    return list(review_dict.values())
