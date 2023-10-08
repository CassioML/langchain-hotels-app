import os
import pandas as pd

import datetime

from common_constants import REVIEWS_TABLE_NAME
from setup.setup_constants import HOTEL_REVIEW_FILE_NAME, FEATURED_INDEX_NAME
from utils.db import get_session, get_keyspace
from utils.reviews import choose_featured

this_dir = os.path.abspath(os.path.dirname(__file__))

insert_review_stmt = None

session = get_session()
keyspace = get_keyspace()


def create_reviews_table():
    session.execute(
        f"""CREATE TABLE IF NOT EXISTS {keyspace}.{REVIEWS_TABLE_NAME} (
                hotel_id text,
                date_added timestamp,
                id text,
                title text,
                body text,
                rating int,
                featured int,
                PRIMARY KEY (hotel_id, date_added, id)
            ) WITH CLUSTERING ORDER BY (date_added DESC, id ASC)"""
    )
    session.execute(
        f"""CREATE CUSTOM INDEX IF NOT EXISTS {FEATURED_INDEX_NAME} ON {keyspace}.{REVIEWS_TABLE_NAME}(featured) 
            USING 'StorageAttachedIndex' """
    )


def parse_date(date_str) -> datetime:
    trunc_date = date_str[: date_str.find("T")]
    return datetime.datetime.strptime(trunc_date, "%Y-%m-%d")


def populate_reviews_table_from_csv():
    # Not batched: all insertions take place concurrently.
    # Take care if you have 100k rows to insert...
    global insert_review_stmt
    if insert_review_stmt is None:
        insert_review_stmt = session.prepare(
            f"""insert into {keyspace}.{REVIEWS_TABLE_NAME} 
                (hotel_id, date_added, id, title, body, rating, featured) values (?, ?, ?, ?, ?, ?, ?)"""
        )

    hotel_review_file_path = os.path.join(this_dir, HOTEL_REVIEW_FILE_NAME)
    hotel_review_data = pd.read_csv(hotel_review_file_path)

    chosen_columns = pd.DataFrame(
        hotel_review_data,
        columns=["hotel_id", "date", "id", "title", "text", "rating", "review_upvotes"],
    )
    review_df = chosen_columns.rename(
        columns={
            # "hotel_id": "hotel_id",
            "date": "date_added",
            # "id": "id",
            # "title": "title",
            "text": "body",
            "review_upvotes": "upvotes",
        }
    )
    review_df["title"] = review_df["title"].fillna("Review")
    review_df["body"] = review_df["body"].fillna("(empty review)")
    review_df["rating"] = review_df["rating"].fillna(5)

    futures = []
    for _, row in review_df.iterrows():
        futures.append(
            session.execute_async(
                insert_review_stmt,
                [
                    row["hotel_id"],
                    parse_date(row["date_added"]),
                    row["id"],
                    row["title"],
                    row["body"],
                    row["rating"],
                    choose_featured(row["upvotes"]),
                ],
            )
        )

    for f in futures:
        f.result()

    print(f"Inserted {len(review_df)} reviews")


if __name__ == "__main__":
    create_reviews_table()
    populate_reviews_table_from_csv()
