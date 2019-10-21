from sqlalchemy import Column, Integer, String

from factionpy.backend.database import Base


class Language(Base):
    __tablename__ = "Language"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
