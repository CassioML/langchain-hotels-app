from utils.db import get_session, get_keyspace
from common_constants import USERS_TABLE_NAME


def create_user_table():
    session = get_session()
    print("session opened")
    keyspace = get_keyspace()
    print("keyspace ", keyspace)

    session.execute(
        f"""create table if not exists {keyspace}.{USERS_TABLE_NAME} (
                            id text primary key,
                            base_preferences text,
                            additional_preferences text, 
                            travel_profile_summary text
                            )"""
    )
    print("table created")


if __name__ == "__main__":
    create_user_table()
