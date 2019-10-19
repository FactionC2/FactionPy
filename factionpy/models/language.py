from sqlalchemy import Column, Integer, String

from factionpy.backend.database import db


class Language(db.Base):
    __tablename__ = "Language"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
