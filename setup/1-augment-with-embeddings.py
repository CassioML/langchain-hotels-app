import os
import json
import argparse
import tqdm
import pandas as pd

from utils.ai import get_embeddings
from utils.reviews import review_body
from setup.embedding_dump import compress_embeddings_map, deflate_embeddings_map

EMBEDDING_FILE_NAME = 'setup/precalculated_embeddings.json'
BATCH_SIZE = 20

if __name__ == '__main__':
    #
    parser = argparse.ArgumentParser(
        description="Augment hotel reviews with embeddings"
    )
    parser.add_argument(
        "-n", metavar="NUM_ROWS", type=int,
        help="Number of rows to process", default=None,
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Force re-computation",
    )
    args = parser.parse_args()

    #
    embeddings = get_embeddings()
    if os.path.isfile(EMBEDDING_FILE_NAME):
        # review_id -> vector, stored specially to shrink size
        enrichment = deflate_embeddings_map(json.load(open(EMBEDDING_FILE_NAME)))
    else:
        enrichment = {}

    #
    hotel_data = pd.read_csv('setup/hotel_reviews.csv')
    #
    todos = []
    for _, row in hotel_data.iterrows():
        id = row['id']
        if id not in enrichment or args.force:
            if args.n is None or len(todos) < args.n:
                todos.append({
                    'id': id,
                    'body': review_body(row),
                })
        if args.n is not None and len(todos) >= args.n:
            break
    
    # browse 'todos' and compute embeddings, then store them to json
    done = 0
    num_batches = (len(todos) + BATCH_SIZE - 1) // BATCH_SIZE
    for batch_index in tqdm.tqdm(range(num_batches)):
        this_batch = todos[BATCH_SIZE*batch_index : BATCH_SIZE*(batch_index+1)]
        bodies = [item['body'] for item in this_batch]
        embedding_vectors = embeddings.embed_documents(bodies)
        #
        for item, vector in zip(this_batch, embedding_vectors):
            enrichment[item['id']] = vector
        #
        with open(EMBEDDING_FILE_NAME, 'w') as o_json:
            json.dump(compress_embeddings_map(enrichment), o_json, indent=4)
        done += len(embedding_vectors)

    print(f'Finished. {done} embeddings computed.')
