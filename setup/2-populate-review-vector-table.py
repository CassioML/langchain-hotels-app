import os
import json
import argparse
import pandas as pd
from itertools import groupby
from typing import Dict, List

import cassio

from setup.embedding_dump import deflate_embeddings_map
from setup.setup_constants import EMBEDDING_FILE_NAME, HOTEL_REVIEW_FILE_NAME

# from utils.reviews import (
#     get_cassio_reviews_vector_table,
#     build_embedded_review_to_store,
# )
from utils.ai import get_embeddings, EMBEDDING_DIMENSION
from utils.db import get_session, get_keyspace
from utils.review_vectors import get_review_vectorstore, REVIEW_VECTOR_TABLE_NAME
from utils.reviews import format_review_content_for_embedding

# We create an ad-hoc "Embeddings" class, sitting on the cache,
# to perform all these insertions idiomatically through the lanchain
# abstraction. This is to avoid having to work at the bare-CassIO lebel
# while still taking advantage of the cache json with precalculated stuff.
from langchain.embeddings.base import Embeddings

class JustCachedEmbeddings(Embeddings):

    def __init__(self, cache_dict: Dict[str, List[float]]) -> None:
        self.cache_dict = cache_dict

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(txt) for txt in texts]

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        if text in self.cache_dict:
            return self.cache_dict[text]
        else:
            # this happens from LangChain when creating the store:
            print(f"**WARNING: embed request for '{text}'. Returning moot results")
            return [0.0] * EMBEDDING_DIMENSION

    async def aembed_query(self, text: str) -> List[float]:
        return self.embed_query(text)


# This script stores the textual data and its embeddings into a table in the database.
# Note: this is a low-level, direct database interaction using cassIO to pre-populate the table. The API uses LangChain.
#
# It expects the following prerequisites:
#  - A vector-enabled database such as AstraDB.
#  - The hotel review CSV file generated in step 0.
#  - The compressed JSON file containing the precalculated embeddings (you can either use the precalculated embeddings
#      in this repo, or run step 1 to calculate them on the fly).
#
# The data is inserted asynchronously in batches to reduce loading time.


this_dir = os.path.abspath(os.path.dirname(__file__))

DEFAULT_BATCH_SIZE = 50


if __name__ == "__main__":
    #
    parser = argparse.ArgumentParser(
        description="Store reviews with embeddings to cassIO vector table"
    )
    parser.add_argument(
        "-n",
        metavar="NUM_ROWS",
        type=int,
        help="Number of rows to insert",
        default=None,
    )
    parser.add_argument(
        "-b",
        metavar="BATCH_SIZE",
        type=int,
        help="Batch size (for concurrent writes)",
        default=DEFAULT_BATCH_SIZE,
    )
    args = parser.parse_args()

    embedding_file_path = os.path.join(this_dir, EMBEDDING_FILE_NAME)
    if os.path.isfile(embedding_file_path):
        # review_id -> vector, which was stored in a compressed format to shrink file size
        enrichment = deflate_embeddings_map(json.load(open(embedding_file_path)))
    else:
        enrichment = {}

    hotel_review_file_path = os.path.join(this_dir, HOTEL_REVIEW_FILE_NAME)
    hotel_review_data = pd.read_csv(hotel_review_file_path)

    # sadly the cache for this "embeddings" must be sentence -> vector,
    # so we need a 'join'
    # (which amounts to a preprocess pass through tne hote reviews)
    text_to_vector_cache = {
        format_review_content_for_embedding(title=row["title"], body=row["text"]): enrichment[row["id"]]
        for _, row in hotel_review_data.iterrows()
        if row["id"] in enrichment
    }
    c_embeddings = JustCachedEmbeddings(cache_dict=text_to_vector_cache)

    # reviews_table = get_cassio_reviews_vector_table()
    db_session = get_session()
    db_keyspace = get_keyspace()
    review_vectorstore = get_review_vectorstore(
        session=db_session,
        keyspace=db_keyspace,
        embeddings=c_embeddings,
    )

    inserted = 0

    eligibles = (
        {
            "text": format_review_content_for_embedding(title=row["title"], body=row["text"]),
            "metadata": {"hotel_id": row["hotel_id"], "rating": row["rating"]},
            "id": row["id"],
            "partition_id": row["hotel_id"],
        }
        for _, row in hotel_review_data.iterrows()
        if row["id"] in enrichment
    )

    def _flush_batch(store, batch):
        if batch:
            # collapse the arguments to lists: {"texts": [...], "ids": [... etc
            texts, metadatas, ids, partition_ids = list(zip(*((
                eli["text"], eli["metadata"], eli["id"], eli["partition_id"]
            ) for eli in batch)))
            # sanity check:
            assert len(set(partition_ids)) == 1
            # we need to group by partition_id and do separate inserts
            review_vectorstore.add_texts(
                texts=texts,
                metadatas=metadatas,
                ids=ids,
                partition_id=partition_ids[0]
            )
        return len(batch)


    groups_by_partition_id = groupby(
        sorted(eligibles, key=lambda eli: eli["partition_id"]),
        key=lambda eli: eli["partition_id"],
    )
    for partition_id, items_in_partition_id in groups_by_partition_id:
        items_list = list(items_in_partition_id)
        # Even within a hotel, we might need to batch insertions:
        this_batch = []
        for eli in items_list:
            this_batch.append(eli)
            if len(this_batch) >= args.b:
                # the batch is full: flush, then increment inserted counter
                inserted += _flush_batch(review_vectorstore, this_batch)
                print(f"  * {inserted} rows written.")
                this_batch = []
            if args.n is not None and inserted >= args.n:
                break
        if args.n is not None and inserted >= args.n:
            break
        # flush any insertions that may be left, then increment inserted counter
        if this_batch:
            inserted += _flush_batch(review_vectorstore, this_batch)
            print(f"  * {inserted} rows written.")
        this_batch = []
    print(f"Finished. {inserted} rows written.")
