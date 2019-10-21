from sqlalchemy import Column, ForeignKey, Integer, String

from factionpy.backend.database import Base


class Module(Base):
    __tablename__ = "Module"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    Description = Column(String)
    BuildCommand = Column(String)
    BuildLocation = Column(String)
    LanguageId = Column(Integer, ForeignKey('Language.Id'))
