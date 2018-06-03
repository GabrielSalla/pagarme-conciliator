import peewee
import peewee_async
import peewee_asyncext
import os
import json

MAX_CONNECTIONS = 5

database_file_name = os.environ["DATABASE_FILE"]
# Load the database access informations
with open(database_file_name, "r") as database_file:
    database_access = json.load(database_file)

# Start connection pool and objects manager
database = peewee_asyncext.PooledPostgresqlExtDatabase(
    **database_access["database-prod"],
    autorollback=True,
    max_connections=MAX_CONNECTIONS,
    register_hstore=False
)

manager = peewee_async.Manager(database)


def close_connections():
    manager.close()
