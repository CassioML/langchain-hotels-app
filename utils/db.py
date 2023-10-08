import os

from dotenv import find_dotenv, load_dotenv
#
import cassio
#
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


dotenv_file = find_dotenv(".env")
load_dotenv(dotenv_file)


cassio_initialized = False


def get_session():
    if not cassio_initialized:
        init_cassio()
    return cassio.config.resolve_session()


def get_keyspace():
    if not cassio_initialized:
        init_cassio()
    return cassio.config.resolve_keyspace()


def init_cassio():
    global cassio_initialized
    # A separate route for a Cassandra cluster session
    use_cassandra = int(os.environ.get("USE_CASSANDRA_CLUSTER", "0"))
    if use_cassandra != 0:
        init_cassio_cassandra()
    else:
        cassio.init(
            token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
            database_id=os.environ["ASTRA_DB_ID"],
            keyspace=os.environ.get("ASTRA_DB_KEYSPACE"),
        )
        cassio_initialized = True


def init_cassio_cassandra():
    global cassio_initialized
    contact_points = [
        cp.strip()
        for cp in os.environ.get("CASSANDRA_CONTACT_POINTS", "").split(',')
        if cp.strip()
    ]
    CASSANDRA_KEYSPACE = os.environ["CASSANDRA_KEYSPACE"]
    CASSANDRA_USERNAME = os.environ.get("CASSANDRA_USERNAME")
    CASSANDRA_PASSWORD = os.environ.get("CASSANDRA_PASSWORD")
    #
    if CASSANDRA_USERNAME and CASSANDRA_PASSWORD:
        auth_provider = PlainTextAuthProvider(
            CASSANDRA_USERNAME,
            CASSANDRA_PASSWORD,
        )
    else:
        auth_provider = None

    c_cluster = Cluster(contact_points if contact_points else None, auth_provider=auth_provider)
    session = c_cluster.connect()
    print("Cassandra session created.")
    #
    cassio.init(
        session=session,
        keyspace=CASSANDRA_KEYSPACE,
    )
    cassio_initialized = True
