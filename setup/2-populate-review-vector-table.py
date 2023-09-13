import os
import json
import argparse
import pandas as pd

import cassio

from setup.embedding_dump import deflate_embeddings_map
from setup.setup_constants import EMBEDDING_FILE_NAME, HOTEL_REVIEW_FILE_NAME

from utils.reviews import review_for_embeddings
from utils.ai import get_embeddings, EMBEDDING_DIMENSION
from utils.db import get_session, get_keyspace
from utils.review_vectors import REVIEW_VECTOR_TABLE_NAME

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

    embeddings = get_embeddings()
    embedding_file_path = os.path.join(this_dir, EMBEDDING_FILE_NAME)
    if os.path.isfile(embedding_file_path):
        # review_id -> vector, which was stored in a compressed format to shrink file size
        enrichment = deflate_embeddings_map(json.load(open(embedding_file_path)))
    else:
        enrichment = {}

    hotel_review_file_path = os.path.join(this_dir, HOTEL_REVIEW_FILE_NAME)
    hotel_data = pd.read_csv(hotel_review_file_path)

    # create cassIO abstraction
    session = get_session()
    keyspace = get_keyspace()
    # TODO: update init signature (auto_id, primary_key_type)
    reviews_table = cassio.table.ClusteredMetadataVectorCassandraTable(
        session=session,
        keyspace=keyspace,
        table=REVIEW_VECTOR_TABLE_NAME,
        vector_dimension=EMBEDDING_DIMENSION,
    )

    #
    inserted = 0

    def _metadata(row):
        return {
            "hotel_id": row["hotel_id"],
            "rating": row["rating"],
        }

    eligibles = (
        {
            "partition_id": row["hotel_id"],
            "body_blob": review_for_embeddings(row["title"], row["text"]),
            "vector": enrichment[row["id"]],
            "row_id": row["id"],
            "metadata": _metadata(row),
        }
        for _, row in hotel_data.iterrows()
        if row["id"] in enrichment
    )

    def _flush_batch(table, batch):
        if batch:
            futures = [table.put_async(**insertion) for insertion in batch]
            for future in futures:
                future.result()
        #
        return len(batch)

    this_batch = []
    for eli in eligibles:
        this_batch.append(eli)
        if len(this_batch) >= args.b:
            # the batch is full: flush, then increment inserted counter
            inserted += _flush_batch(reviews_table, this_batch)
            print(f"  * {inserted} rows written.")
            this_batch = []
        if args.n is not None and inserted >= args.n:
            break
    # flush any insertions that may be left, then increment inserted counter
    inserted += _flush_batch(reviews_table, this_batch)
    this_batch = []

    print(f"Finished. {inserted} rows written.")
