"""Utilities to manipulate reviews"""

from common_constants import FEATURED_VOTE_THRESHOLD


def review_body(review):
    return f"{review['title']}: {review['text']}"


def choose_featured(num_upvotes) -> int:
    if num_upvotes > FEATURED_VOTE_THRESHOLD:
        return 1
    else:
        return 0