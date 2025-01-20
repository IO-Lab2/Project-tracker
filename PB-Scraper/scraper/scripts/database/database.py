from dotenv import load_dotenv, find_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection
from scrapy.exceptions import DropItem #temp

from os import getenv
from logging import getLogger

#temp
#from select import does_row_exist

logger = getLogger(__name__)

class EnvVarNotFound(Exception):
    pass

#for loading .env
#loads only if it hasn't been loaded already
#raises EnvVarNotFound if .env fails to load
def load_env():
    if getenv("PGPORT") is None:
        path = find_dotenv()
        was_successful = load_dotenv(dotenv_path=path)
        if not was_successful:
            raise EnvVarNotFound("load_env: could not load .env")
    #end of load_env


#returns a new connection and automatically registers it
#raises EnvVarNotFound if .env cannot not be loaded
#raises psycopg2.Error or psycopg2.Warning from psycopg2.connect() if sth goes wrong
def make_connection():
    load_env()
    conn = connect(
        dbname=getenv("PGDATABASE"),
        user=getenv("PGUSER"),
        password=getenv("PGPASSWORD"),
        host=getenv("PGHOST"),
        port=getenv("PGPORT"),
        sslmode=getenv("PGSSLMODE")
    )
    logger.debug("make_connection: making a connection was successful")
    return conn
    #end of make_connection
