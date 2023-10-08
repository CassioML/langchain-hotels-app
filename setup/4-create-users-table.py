from utils.db import get_session, get_keyspace
from common_constants import USERS_TABLE_NAME

session = get_session()
keyspace = get_keyspace()


def create_user_table():
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
