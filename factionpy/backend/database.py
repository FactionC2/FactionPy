from time import sleep
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Table, LargeBinary, DateTime, Boolean, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship
from factionpy.logger import log
from factionpy.config import get_config_value

DB_URI = None
db_connected = False
db = None

if get_config_value("POSTGRES_DATABASE"):
    DB_URI = "postgresql://{}:{}@{}/{}?client_encoding=utf8".format(
        get_config_value("POSTGRES_USERNAME"), get_config_value("POSTGRES_PASSWORD"),
        get_config_value("POSTGRES_HOST"), get_config_value("POSTGRES_DATABASE")
    )


class DBClient:
    engine = create_engine(DB_URI)
    session_init = sessionmaker(bind=engine)
    Base = declarative_base()
    session = session_init()


if DB_URI:
    log("database.py", "Checking Database..", "debug")
    while not db_connected:
        try:
            db_connection = psycopg2.connect(DB_URI, connect_timeout=5)
            db_connection.cursor()
            db_connected = True
            log("database.py", "Database is up!", "debug")
            db_connection.close()
        except Exception as e:
            log("database.py", "Database not reachable, will wait. Error: {0}".format(str(e)), "debug")
            db_connected = False
            sleep(5)
    log("database.py", "Configuring DB object..", "debug")
    db = DBClient()
