import os
import json
import argparse
import pandas as pd

import cassio

from embedding_dump import compress_embeddings_map, deflate_embeddings_map
from setup_constants import EMBEDDING_FILE_NAME, HOTEL_REVIEW_FILE_NAME

from utils.reviews import review_body
from utils.ai import EMBEDDING_DIMENSION
from utils.db import get_session, get_keyspace
from utils.review_vectors import REVIEW_VECTOR_TABLE_NAME

BATCH_SIZE = 10

if __name__ == '__main__':
    #
    parser = argparse.ArgumentParser(
        description="Store reviews with embeddings to cassIO vector table"
    )
    parser.add_argument(
        "-n", metavar="NUM_ROWS", type=int,
        help="Number of rows to insert", default=None,
    )
    args = parser.parse_args()

    if os.path.isfile(EMBEDDING_FILE_NAME):
        # review_id -> vector, stored specially to shrink size
        enrichment = deflate_embeddings_map(json.load(open(EMBEDDING_FILE_NAME)))
    else:
        enrichment = {}

    hotel_data = pd.read_csv(HOTEL_REVIEW_FILE_NAME)

    # create cassIO abstraction
    session = get_session()
    keyspace = get_keyspace()
    # TODO: update init signature (auto_id, primary_key_type)
    # Note: this is a "low-level", direct cassIO usage. The API uses LangChain.
    reviews_table = cassio.vector.VectorTable(
        session=session,
        keyspace=keyspace,
        table=REVIEW_VECTOR_TABLE_NAME,
        embedding_dimension=EMBEDDING_DIMENSION,
        auto_id=False,
    )
    #
    inserted = 0

    def _metadata(row):
        return {
            'hotel_id': row['hotel_id'],
            'rating': row['rating'],
        }

    eligibles = (
        {
            'document': review_body(row),
            'embedding_vector': enrichment[row['id']],
            'document_id': row['id'],
            'metadata': _metadata(row),
            'ttl_seconds': None,
        }
        for _, row in hotel_data.iterrows()
        if row['id'] in enrichment
    )

    def _flush_batch(table, batch):
        if batch:
            futures = [
                table.put_async(**insertion)
                for insertion in batch
            ]
            for future in futures:
                future.result()
        #
        return len(batch)

    this_batch = []
    for eli in eligibles:
        this_batch.append(eli)
        if len(this_batch) >= BATCH_SIZE:
            # flush, increment inserted
            inserted += _flush_batch(reviews_table, this_batch)
            this_batch = []
        if args.n is not None and inserted >= args.n:
            break
    # flush, increment inserted
    inserted += _flush_batch(reviews_table, this_batch)
    this_batch = []

    print(f'Finished. {inserted} rows written.')
