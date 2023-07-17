import pandas as pd

from common_constants import HOTEL_TABLE_NAME
from setup_constants import HOTEL_REVIEW_FILE_NAME
from utils.db import get_session, get_keyspace


def create_hotel_table_with_index():
    session = get_session()
    keyspace = get_keyspace()

    session.execute(f"""create table if not exists {keyspace}.{HOTEL_TABLE_NAME} (
                            id text primary key,
                            name text, 
                            city text, 
                            country text)""")

    session.execute(f"""create custom index if not exists name_sai_idx on {keyspace}.{HOTEL_TABLE_NAME} (name) 
                            using 'StorageAttachedIndex'""")
    session.execute(f"""create custom index if not exists city_sai_idx on {keyspace}.{HOTEL_TABLE_NAME} (city) 
                            using 'StorageAttachedIndex'""")
    session.execute(f"""create custom index if not exists country_sai_idx on {keyspace}.{HOTEL_TABLE_NAME} (country) 
                            using 'StorageAttachedIndex'""")


def populate_hotel_table_from_csv():
    session = get_session()
    keyspace = get_keyspace()

    hotel_review_data = pd.read_csv(HOTEL_REVIEW_FILE_NAME)

    insert_hotel_stmt = session.prepare(f"insert into {keyspace}.{HOTEL_TABLE_NAME} (id, name, city, country) values (?, ?, ?, ?)")

    inserted_hotel_ids = set()

    for _, row in hotel_review_data.iterrows():
        hotel_id = row['hotel_id']
        if hotel_id not in inserted_hotel_ids:
            session.execute_async(insert_hotel_stmt, (hotel_id, row['hotel_name'], row['hotel_city'], row['hotel_country']))
            inserted_hotel_ids.add(hotel_id)
    print(f"Inserted {len(inserted_hotel_ids)} hotels")


create_hotel_table_with_index()
populate_hotel_table_from_csv()

