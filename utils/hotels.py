from utils.db import get_session, get_keyspace

from common_constants import HOTELS_TABLE_NAME
from typing import List
from utils.models import Hotel

find_hotels_prepared_stmt = None


def get_find_hotels_prepared_statement():
    global find_hotels_prepared_stmt

    session = get_session()
    keyspace = get_keyspace()

# TODO decide if we want to have a limit on the hotels, and if so, how large + extract it to a constant
    if not find_hotels_prepared_stmt:
        find_hotels_prepared_stmt = session.prepare(
            f"SELECT id, name FROM {keyspace}.{HOTELS_TABLE_NAME} where city = ? and country = ? limit 10"
        )

    return find_hotels_prepared_stmt


def find_hotels_by_location(city: str, country: str) -> List[Hotel]:
    session = get_session()

    find_hotels_prep_stmt = get_find_hotels_prepared_statement()

    hotel_rows = session.execute(find_hotels_prep_stmt, (city, country))

    hotels = list({})
    for row in hotel_rows:
        hotels.append(Hotel(city=city, country=country, name=row.name, id=row.id))

    return hotels
