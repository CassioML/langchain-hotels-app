from utils.db import get_session, get_keyspace

from common_constants import HOTELS_TABLE_NAME
from typing import List, Optional
from utils.models import Hotel

find_hotels_stmt = None
find_hotel_by_id_stmt = None


def get_find_hotels_prepared_statement():
    return find_hotels_stmt


def find_hotels_by_location(city: str, country: str) -> List[Hotel]:
    global find_hotels_stmt

    session = get_session()
    keyspace = get_keyspace()

    # TODO decide if we want to have a limit on the hotels, and if so, how large + extract it to a constant
    if not find_hotels_stmt:
        find_hotels_stmt = session.prepare(
            f"SELECT id, name FROM {keyspace}.{HOTELS_TABLE_NAME} where city = ? and country = ? limit 15"
        )

    hotel_rows = session.execute(find_hotels_stmt, (city, country))

    hotels = [
        Hotel(city=city, country=country, name=row.name, id=row.id)
        for row in hotel_rows
    ]

    return hotels


def find_hotel_by_id(hotel_id: str) -> Optional[Hotel]:
    global find_hotel_by_id_stmt

    session = get_session()
    keyspace = get_keyspace()

    # TODO decide if we want to have a limit on the hotels, and if so, how large + extract it to a constant
    if not find_hotel_by_id_stmt:
        find_hotel_by_id_stmt = session.prepare(
            f"SELECT name, city, country FROM {keyspace}.{HOTELS_TABLE_NAME} where id = ?"
        )

    row = session.execute(find_hotel_by_id_stmt, (hotel_id,)).one()

    if row is not None:
        return Hotel(city=row.city, country=row.country, name=row.name, id=hotel_id)
    else:
        return None
