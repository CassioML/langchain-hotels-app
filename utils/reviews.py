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

# TODO add function to retrieve reviews relevant to a user


# ### ADDING REVIEWS

# Entry point for when we want to add a review
# - Generates an id for the new review
# - Stores the review in the non-vectorised table
# - Embeds the review and then stores it in the vectorised table
def insert_review_for_hotel(
    hotel_id: str, review_title: str, review_body: str
):
    review_id = generate_review_id()
    insert_into_reviews_table(hotel_id, review_id, review_title, review_body)

    hotel = find_hotel_by_id(hotel_id)

    # TODO check that the hotel was found

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
        "rating": hotel.rating,
    }

    review_store.add_texts(
        texts=[format_review_content_for_embedding(review_title, review_body)],
        metadatas=[review_metadata],
        ids=[review_id],
        partition_id=hotel_id,
    )

    # embedded_review = embed_review(
    #     hotel_id=hotel_id,
    #     hotel_rating=hotel.rating,
    #     review_id=review_id,
    #     review_title=review_title,
    #     review_body=review_body,
    # )
    # insert_into_reviews_vector_table(embedded_review)


def generate_review_id():
    return uuid.uuid4().hex


def format_review_content_for_embedding(title: str, body: str) -> str:
    return f"{title}: {body}"


# def create_review_doc_for_embedding(review_id: str, review_title: str, review_body: str) -> {}:
#     return {
#         "id": review_id,
#         "body": format_review_content_for_embedding(review_title, review_body),
#     }


def choose_featured(num_upvotes: int) -> int:
    if num_upvotes > FEATURED_VOTE_THRESHOLD:
        return 1
    else:
        return 0


# def get_cassio_reviews_vector_table() -> (
#     cassio.table.ClusteredMetadataVectorCassandraTable
# ):
#     # create cassIO abstraction
#     session = get_session()
#     keyspace = get_keyspace()
#     # TODO: update init signature (auto_id, primary_key_type)
#     reviews_table = cassio.table.ClusteredMetadataVectorCassandraTable(
#         session=session,
#         keyspace=keyspace,
#         table=REVIEW_VECTOR_TABLE_NAME,
#         vector_dimension=EMBEDDING_DIMENSION,
#     )
#     return reviews_table


def insert_into_reviews_table(
    hotel_id: str, review_id: str, review_title: str, review_body: str
):
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

    session.execute(
        insert_review_stmt,
        (hotel_id, date_added, review_id, review_title, review_body, featured),
    )


# def insert_into_reviews_vector_table(embedded_review: Dict):
#     reviews_vector_table = get_cassio_reviews_vector_table()
#     reviews_vector_table.put_async(**embedded_review)


# TODO figure out type hint for vector
# here and in populate-review-vector-table
# def build_embedded_review_to_store(
#     hotel_id: str,
#     hotel_rating: str,
#     review_id: str,
#     review_vector,
#     review_title: str,
#     review_body: str,
# ) -> {}:

#     review_metadata = {
#         "hotel_id": hotel_id,
#         "rating": hotel_rating,
#     }
#     embedded = {
#         "partition_id": hotel_id,
#         "body_blob": format_review_content_for_embedding(title=review_title, body=review_body),
#         "vector": review_vector,
#         "row_id": review_id,
#         "metadata": review_metadata,
#     }
#     return embedded


# def embed_review(
#     hotel_id: str,
#     hotel_rating: str,
#     review_id: str,
#     review_title: str,
#     review_body: str,
# ) -> {}:
#     embeddings = get_embeddings()

#     review_doc = create_review_doc_for_embedding(review_id=review_id, review_title=review_title, review_body=review_body)
#     vector = embeddings.embed_documents([review_doc["body"]])[0]
#     return build_embedded_review_to_store(
#         hotel_id, hotel_rating, review_id, vector, review_title, review_body
#     )



