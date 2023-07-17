from db import get_session, get_keyspace

from common_constants import HOTEL_TABLE_NAME

find_hotels_prepared_stmt = None


def get_find_hotels_prepared_statement():
    global find_hotels_prepared_stmt

    session = get_session()
    keyspace = get_keyspace()

    if not find_hotels_prepared_stmt:
        find_hotels_prepared_stmt = session.prepare(f"""SELECT id, name from {keyspace}.{HOTEL_TABLE_NAME} 
                                                            where city = ? and country = ?""")

    return find_hotels_prepared_stmt


# TODO add type hint for return type
def find_hotels_by_location(city: str, country: str):
    session = get_session()

    find_hotels_prep_stmt = get_find_hotels_prepared_statement()

    hotel_rows = session.execute(find_hotels_prep_stmt, (city, country))

    hotels = list({})
    for row in hotel_rows:
        hotels.append({'id': row['id'],
                       'name': row['name']})

    return hotels

