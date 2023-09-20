"""Utilities to manipulate reviews"""
import random
import uuid, datetime
from langchain.vectorstores import Cassandra, VectorStore

from common_constants import (
    FEATURED_VOTE_THRESHOLD,
    REVIEWS_TABLE_NAME,
    REVIEW_VECTOR_TABLE_NAME,
)
from utils.models import HotelReview

from utils.ai import get_embeddings
from utils.db import get_session, get_keyspace

from typing import List

# LangChain VectorStore abstraction to interact with the vector database
review_vectorstore = None


def get_review_vectorstore(session, keyspace, embeddings, is_setup: bool = False):
    global review_vectorstore
    if review_vectorstore is None:
        review_vectorstore = Cassandra(
            embedding=embeddings,
            session=session,
            keyspace=keyspace,
            table_name=REVIEW_VECTOR_TABLE_NAME,
            partition_id="will-always-be-overridden",
            partitioned=True,
            skip_provisioning=not is_setup,
        )
    return review_vectorstore


# ### SELECTING REVIEWS

# Prepared statements for selecting reviews
select_recent_reviews_stmt = None
select_featured_reviews_stmt = None


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
        review_dict[row.id] = HotelReview(
            id=row.id, title=row.title, body=row.body, rating=row.rating
        )

    global select_featured_reviews_stmt
    if select_featured_reviews_stmt is None:
        select_featured_reviews_stmt = session.prepare(
            f"SELECT id, title, body, rating FROM {keyspace}.{REVIEWS_TABLE_NAME} WHERE hotel_id = ? and featured = 1 LIMIT 3"
        )

    rows_featured = session.execute(select_recent_reviews_stmt, (hotel_id,))
    for row in rows_featured:
        review_dict[row.id] = HotelReview(
            id=row.id, title=row.title, body=row.body, rating=row.rating
        )

    return list(review_dict.values())


# TODO add function to retrieve reviews relevant to a user


# ### ADDING REVIEWS

# Prepared statement for inserting reviews
insert_review_stmt = None


# Entry point for when we want to add a review
# - Generates an id for the new review
# - Stores the review in the non-vectorised table
# - Embeds the review and then stores it in the vectorised table
def insert_review_for_hotel(
    hotel_id: str, review_title: str, review_body: str, review_rating: int
):
    review_id = generate_review_id()
    insert_into_reviews_table(
        hotel_id, review_id, review_title, review_body, review_rating
    )
    insert_into_review_vector_table(
        hotel_id, review_id, review_title, review_body, review_rating
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


# Inserts a new review into the non-vectorized reviews table
def insert_into_reviews_table(
    hotel_id: str,
    review_id: str,
    review_title: str,
    review_body: str,
    review_rating: int,
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
        (
            hotel_id,
            date_added,
            review_id,
            review_title,
            review_body,
            review_rating,
            featured,
        ),
    )


# Inserts a new review into the vectorized reviews table, using a VectorStore of type Cassandra from LangChain
def insert_into_review_vector_table(
    hotel_id: str,
    review_id: str,
    review_title: str,
    review_body: str,
    review_rating: int,
):
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


def find_similar_reviews(query_review: str, hotel_id: str, store: VectorStore):
    # return a list of (dict-shaped) rows from the vector store
    docs = store.similarity_search(query_review, k=3, partition_id=hotel_id)
    return [doc.page_content for doc in docs]
