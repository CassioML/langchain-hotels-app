import pandas as pd

from common_constants import HOTELS_TABLE_NAME
from setup.setup_constants import HOTEL_REVIEW_FILE_NAME
from utils.db import get_session, get_keyspace

insert_hotel_stmt = None


def create_hotel_table():
    session = get_session()
    keyspace = get_keyspace()

    session.execute(
        f"""create table if not exists {keyspace}.{HOTELS_TABLE_NAME} (
                            country text,
                            city text, 
                            id text,
                            name text,
                            latitude float,
                            longitude float,
                            primary key (( country, city), id )
                            )"""
    )


def populate_hotel_table_from_csv():
    # Not batched: all insertions take place concurrently.
    # Take care if you have 100k hotels to insert...

    session = get_session()
    keyspace = get_keyspace()

    global insert_hotel_stmt
    if insert_hotel_stmt is None:
        insert_hotel_stmt = session.prepare(
            f"insert into {keyspace}.{HOTELS_TABLE_NAME} (id, name, city, country, latitude, longitude) values (?, ?, ?, ?, ?, ?)"
        )

    hotel_review_data = pd.read_csv(HOTEL_REVIEW_FILE_NAME)
    chosen_columns = pd.DataFrame(
        hotel_review_data,
        columns=[
            "hotel_id",
            "hotel_name",
            "hotel_city",
            "hotel_country",
            "hotel_latitude",
            "hotel_longitude",
        ],
    )
    renamed_columns = chosen_columns.rename(
        columns={
            "hotel_id": "id",
            "hotel_name": "name",
            "hotel_city": "city",
            "hotel_country": "country",
            "hotel_latitude": "latitude",
            "hotel_longitude": "longitude",
        }
    )
    hotel_df = renamed_columns.drop_duplicates()

    futures = []
    for _, row in hotel_df.iterrows():
        futures.append(
            session.execute_async(
                insert_hotel_stmt,
                [
                    row[f]
                    for f in ["id", "name", "city", "country", "latitude", "longitude"]
                ],
            )
        )

    for f in futures:
        f.result()

    print(f"Inserted {len(hotel_df)} hotels")


if __name__ == "__main__":
    create_hotel_table()
    populate_hotel_table_from_csv()
