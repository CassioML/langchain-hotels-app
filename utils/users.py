import json

from utils.db import get_session, get_keyspace

from common_constants import USERS_TABLE_NAME

"""for now by hand:

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    profile TEXT,
    auto_description TEXT,
);
"""

# TODO: prepare statements and cache them

def read_user_profile(user_id):

    session = get_session()
    keyspace = get_keyspace()

    user_row = session.execute(f"SELECT profile FROM {keyspace}.{USERS_TABLE_NAME} WHERE id=%s", (user_id,)).one()
    if user_row:
        return json.loads(user_row.profile)
    else:
        return {}

def write_user_profile(user_id, profile):
    session = get_session()
    keyspace = get_keyspace()

    session.execute(
        f"INSERT INTO {keyspace}.{USERS_TABLE_NAME} (id, profile) VALUES (%s, %s);",
        (user_id, json.dumps(profile)),
    )

def update_user_desc(user_id, profile):
    import time
    print("STARTING FOR ", user_id)
    time.sleep(2)  # instead of an LLM or something
    fake_desc = ", ".join("%s=%s" % (k.upper(), "yes" if v else "no") for k, v in profile.items())

    # write:
    session = get_session()
    keyspace = get_keyspace()

    session.execute(
        f"INSERT INTO {keyspace}.{USERS_TABLE_NAME} (id, auto_description) VALUES (%s, %s);",
        (user_id, fake_desc),
    )
