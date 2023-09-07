from langchain.vectorstores.cassandra import Cassandra
from langchain.vectorstores import VectorStore

REVIEW_VECTOR_TABLE_NAME = "hotel_reviews_embeddings"

review_vectorstore = None


def get_review_vectorstore(session, keyspace, embeddings, hotel_id):
    global review_vectorstore
    if review_vectorstore is None:
        review_vectorstore = Cassandra(
            embedding=embeddings,
            session=session,
            keyspace=keyspace,
            table_name=REVIEW_VECTOR_TABLE_NAME,
            partitioned=True,
            partition_id=hotel_id,
            skip_provisioning=True,
        )
    return review_vectorstore


def find_similar_reviews(query_review: str, store: VectorStore):
    # return a list of (dict-shaped) rows from the vector store
    docs = store.similarity_search(query_review, k=3)
    return [doc.page_content for doc in docs]
