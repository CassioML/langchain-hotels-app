from typing import List

from cassandra.query import PreparedStatement
from cassandra.cluster import Session

from common_constants import HOTEL_TABLE_NAME
from utils.models import Hotel

SELECT_HOTEL_BY_COUNTRY_CITY_CQL = "SELECT country, city, id, name FROM {keyspace}.{table} WHERE COUNTRY = ? AND CITY = ? LIMIT 20;"

prepared_statement_cache = {}


def _get_prepared(session, statement_str):
    global prepared_statement_cache
    # handle a cache of prep.statements
    if statement_str not in prepared_statement_cache:
        prepared_statement_cache[statement_str] = session.prepare(statement_str)
    return prepared_statement_cache[statement_str]


def find_hotels_by_country_city(session: Session, keyspace: str, country: str, city: str) -> List[Hotel]:
    stmt_str = SELECT_HOTEL_BY_COUNTRY_CITY_CQL.format(keyspace=keyspace, table=HOTEL_TABLE_NAME)
    stmt = _get_prepared(session, stmt_str)
    result_set = session.execute(stmt, (country, city))
    return [
        Hotel(**result._asdict())
        for result in result_set
    ]
