from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from factionpy.backend.database import Base


class CommandParameter(Base):
    __tablename__ = "CommandParameter"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    Help = Column(String)
    Required = Column(Boolean)
    Position = Column(Integer)
    Values = Column(String)
    CommandId = Column(Integer, ForeignKey('Command.Id'))
