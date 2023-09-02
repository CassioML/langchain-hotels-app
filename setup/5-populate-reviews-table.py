import pandas as pd

import datetime

from common_constants import REVIEWS_TABLE_NAME
from setup.setup_constants import HOTEL_REVIEW_FILE_NAME
from utils.db import get_session, get_keyspace

insert_review_stmt = None


def create_reviews_table():
    session = get_session()
    keyspace = get_keyspace()

    session.execute(
        f"""create table if not exists {keyspace}.{REVIEWS_TABLE_NAME} (
                hotel_id text,
                date_added timestamp,
                id text,
                review_text text,
                upvotes int,
                PRIMARY KEY (hotel_id, date_added, id)
            ) WITH CLUSTERING ORDER BY (date_added DESC, id ASC)"""
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
                (hotel_id, date_added, id, review_text, upvotes) values (?, ?, ?, ?, ?)"""
        )

    hotel_review_data = pd.read_csv(HOTEL_REVIEW_FILE_NAME)
    
    chosen_columns = pd.DataFrame(
        hotel_review_data,
        columns=["hotel_id", "date", "id", "text", "review_upvotes"],
    )
    review_df = chosen_columns.rename(
        columns={
            "hotel_id": "hotel_id",
            "date": "date_added",
            "id": "id",
            "text": "review_text",
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
                    row["review_text"],
                    row["upvotes"],
                ],
            )
        )

    for f in futures:
        f.result()

    print(f"Inserted {len(review_df)} reviews")


if __name__ == "__main__":
    create_reviews_table()
    populate_reviews_table_from_csv()
