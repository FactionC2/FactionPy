from time import sleep
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Table, LargeBinary, DateTime, Boolean, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship
from factionpy.logger import log
from factionpy.config import get_config_value

Base = declarative_base()


class DBClient:
    engine = None
    db_uri = None
    session_init = None
    session = None

    def __init__(self):
        db_connected = False

        if get_config_value("POSTGRES_DATABASE"):
            self.db_uri = "postgresql://{}:{}@{}/{}?client_encoding=utf8".format(
                get_config_value("POSTGRES_USERNAME"), get_config_value("POSTGRES_PASSWORD"),
                get_config_value("POSTGRES_HOST"), get_config_value("POSTGRES_DATABASE")
            )
            while not db_connected:
                try:
                    db_connection = psycopg2.connect(self.db_uri, connect_timeout=5)
                    db_connection.cursor()
                    db_connected = True
                    log("database.py", "Database is up!", "debug")
                    db_connection.close()
                    self.engine = create_engine(self.db_uri)
                    self.Base = declarative_base()
                    session_init = sessionmaker(bind=self.engine)
                    self.session = session_init()
                except Exception as e:
                    log("database.py", "Database not reachable, will wait. Error: {0}".format(str(e)), "debug")
                    db_connected = False
                    sleep(5)
        else:
            log("database.py", "Could not get POSTGRES_DATABASE from config. Can not create DBClient")
