from time import sleep
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, LargeBinary, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from factionpy.logger import log
from factionpy.config import DB_URI

db_connected = False
log("database.py", "Checking Database..")
while not db_connected:
    try:
        db_connection = psycopg2.connect(DB_URI, connect_timeout=5)
        db_connection.cursor()
        db_connected = True
        log("database.py", "Database is up!")
        db_connection.close()
    except Exception as e:
        log("database.py", "Database not reachable, will wait. Error: {0}".format(str(e)))
        db_connected = False
        sleep(5)

log("database.py", "Configuring DB object..")


class DBClient:
    engine = create_engine(DB_URI)
    session = sessionmaker(bind=engine)
    Base = declarative_base()
    Column = Column,
    String = String,
    LargeBinary = LargeBinary,
    DateTime = DateTime,
    Boolean = Boolean,
    ForeignKey = ForeignKey,
    relationship = relationship


db = DBClient()
