from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from factionpy.backend.database import db
from factionpy.models.command_parameter import CommandParameter


class Command(db.Base):
    __tablename__ = "Command"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    Description = Column(String)
    Help = Column(String)
    MitreReference = Column(String)
    OpsecSafe = Column(Boolean)
    ModuleId = Column(Integer, ForeignKey('Module.Id'))
    AgentTypeId = Column(Integer, ForeignKey('AgentType.Id'))
    Parameters = relationship('CommandParameter', backref='Command', lazy=True)
