
import pymongo
from mongodb_proxy import MongoProxy


def connect_to_mongodb(
    db, collection, host,
    port=27017, tz_aware=True, user=None, password=None, retry_wait_time=0.1, proxy=True, **kwargs
):
    """
    Returns a MongoDB Database connection, optionally wrapped in a proxy. The proxy
    handles AutoReconnect errors by retrying read operations, since these exceptions
    typically indicate a temporary step-down condition for MongoDB.
    """
    mongo_conn = pymongo.database.Database(
        pymongo.MongoClient(
            host=host,
            port=port,
            tz_aware=tz_aware,
            document_class=dict,
            **kwargs
        ),
        db
    )

    if proxy:
        mongo_conn = MongoProxy(
            mongo_conn,
            wait_time=retry_wait_time
        )

    # If credentials were provided, authenticate the user.
    if user is not None and password is not None:
        mongo_conn.authenticate(user, password)

    return mongo_conn
