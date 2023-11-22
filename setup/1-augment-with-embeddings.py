import os
import json
import argparse
import tqdm
import pandas as pd

from utils.ai import get_embeddings
from utils.reviews import format_review_content_for_embedding
from setup.embedding_dump import compress_embeddings_map, deflate_embeddings_map
from setup.setup_constants import EMBEDDING_FILE_NAME, HOTEL_REVIEW_FILE_NAME

# Important note:
# This step can be skipped if using the precalculated embeddings available as part of the setup assets.
# Note that the call to embed data contained in this script is likely to incur a financial cost.
#
# Script that embeds the review data contained in the CSV file cleaned up at the previous step.
# If some of the data has already been embedded, this script will skip it to avoid re-embedding it unnecessarily.
#
# This script performs the following operations:
#  - Loads the already-embedded data, if any.
#  - Loops over the contents of the hotel review CSV, identifying the reviews that have not yet been embedded.
#  - Embeds those reviews and stores them to a JSON file, with the review_id as document id and the vector as content.
#
# The resulting JSON file is compressed in order to reduce storage footprint.


this_dir = os.path.abspath(os.path.dirname(__file__))

BATCH_SIZE = 20

if __name__ == "__main__":
    #
    parser = argparse.ArgumentParser(
        description="Augment hotel reviews with embeddings"
    )
    parser.add_argument(
        "-n",
        metavar="NUM_ROWS",
        type=int,
        help="Number of rows to process",
        default=None,
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force re-computation",
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
    hotel_review_data = pd.read_csv(hotel_review_file_path)

    reviews_to_embed = []
    for _, row in hotel_review_data.iterrows():
        review_id = row["id"]
        if review_id not in enrichment or args.force:
            if args.n is None or len(reviews_to_embed) < args.n:
                reviews_to_embed.append(
                    {
                        "id": review_id,
                        "body": format_review_content_for_embedding(
                            title=row["title"],
                            body=row["text"],
                        ),
                    }
                )
        if args.n is not None and len(reviews_to_embed) >= args.n:
            break

    # scan 'todos' and compute embeddings, then store them to json
    done = 0
    num_batches = (len(reviews_to_embed) + BATCH_SIZE - 1) // BATCH_SIZE
    for batch_index in tqdm.tqdm(range(num_batches)):
        this_batch = reviews_to_embed[
            BATCH_SIZE * batch_index : BATCH_SIZE * (batch_index + 1)
        ]
        bodies = [item["body"] for item in this_batch]
        embedding_vectors = embeddings.embed_documents(bodies)
        #
        for item, vector in zip(this_batch, embedding_vectors):
            enrichment[item["id"]] = vector
        #
        with open(embedding_file_path, "w") as o_json:
            json.dump(compress_embeddings_map(enrichment), o_json, indent=4)
        done += len(embedding_vectors)

    print(f"[1-augment-with-embeddings.py] Finished. {done} embeddings computed and stored to '{embedding_file_path}'.")
