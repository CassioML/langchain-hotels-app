"""Utilities to manipulate reviews"""

def review_body(review):
    return f"{review['title']}: {review['text']}"
