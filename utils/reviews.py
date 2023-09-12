"""Utilities to manipulate reviews"""

from common_constants import FEATURED_VOTE_THRESHOLD, REVIEWS_TABLE_NAME
from utils.models import HotelReview

from utils.db import get_session, get_keyspace

from typing import List

select_recent_reviews_stmt = None
select_featured_reviews_stmt = None


def review_for_embeddings(title, body):
    return f"{title}: {body}"


def choose_featured(num_upvotes) -> int:
    if num_upvotes > FEATURED_VOTE_THRESHOLD:
        return 1
    else:
        return 0


def select_reviews(hotel_id) -> List[HotelReview]:
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

