import pandas as pd

import datetime

from common_constants import REVIEWS_TABLE_NAME
from setup.setup_constants import HOTEL_REVIEW_FILE_NAME, FEATURED_INDEX_NAME
from utils.db import get_session, get_keyspace
from utils.reviews import choose_featured

insert_review_stmt = None


def create_reviews_table():
    session = get_session()
    keyspace = get_keyspace()

    session.execute(
        f"""CREATE TABLE IF NOT EXISTS {keyspace}.{REVIEWS_TABLE_NAME} (
                hotel_id text,
                date_added timestamp,
                id text,
                title text,
                content text,
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
    # Take care if you have 100k hotels to insert...

    session = get_session()
    keyspace = get_keyspace()

    global insert_review_stmt
    if insert_review_stmt is None:
        insert_review_stmt = session.prepare(
            f"""insert into {keyspace}.{REVIEWS_TABLE_NAME} 
                (hotel_id, date_added, id, title, content, featured) values (?, ?, ?, ?, ?, ?)"""
        )

    hotel_review_data = pd.read_csv(HOTEL_REVIEW_FILE_NAME)
    
    chosen_columns = pd.DataFrame(
        hotel_review_data,
        columns=["hotel_id", "date", "id", "title", "text", "review_upvotes"],
    )
    review_df = chosen_columns.rename(
        columns={
            "hotel_id": "hotel_id",
            "date": "date_added",
            "id": "id",
            "title": "title",
            "text": "content",
            "review_upvotes": "upvotes",
        }
    )

    futures = []
    for _, row in review_df.iterrows():
        futures.append(
            session.execute_async(
                insert_review_stmt,
                [
                    row["hotel_id"],
                    parse_date(row["date_added"]),
                    row["id"],
                    str(row["title"]),
                    str(row["content"]),
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
