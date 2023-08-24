import os
import atexit

from dotenv import find_dotenv, load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

dotenv_file = find_dotenv(".env")
load_dotenv(dotenv_file)

ASTRA_DB_SECURE_BUNDLE_PATH = os.environ["ASTRA_DB_SECURE_BUNDLE_PATH"]
ASTRA_DB_APPLICATION_TOKEN = os.environ["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_KEYSPACE = os.environ["ASTRA_DB_KEYSPACE"]


cluster = None
session = None


def get_session():
    #
    global session
    global cluster
    #
    if session is None:
        print("[get_session] Creating session")
        cluster = Cluster(
            cloud={
                "secure_connect_bundle": ASTRA_DB_SECURE_BUNDLE_PATH,
            },
            auth_provider=PlainTextAuthProvider(
                "token",
                ASTRA_DB_APPLICATION_TOKEN,
            ),
        )
        session = cluster.connect()
    #
    return session


def get_keyspace():
    return ASTRA_DB_KEYSPACE


@atexit.register
def shutdown_driver():
    if session is not None:
        print("[shutdown_driver] Closing connection")
        cluster.shutdown()
        session.shutdown()
