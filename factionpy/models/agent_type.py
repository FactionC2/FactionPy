from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from factionpy.backend.database import Base

from factionpy.models.agent_type_format import AgentTypeFormat
from factionpy.models.agent_type_architecture import AgentTypeArchitecture
from factionpy.models.agent_type_configuration import AgentTypeConfiguration
from factionpy.models.agent_type_operating_system import AgentTypeOperatingSystem
from factionpy.models.agent_type_version import AgentTypeVersion
from factionpy.models.agent_transport_type import AgentTransportType
from factionpy.models.payload import Payload
from factionpy.models.command import Command


class AgentType(Base):
    __tablename__ = "AgentType"
    Id = Column(Integer, primary_key=True)
    Agents = relationship('Agent', backref='AgentType', lazy=True)
    Payloads = relationship('Payload', backref='AgentType', lazy=True)
    AgentTransportTypes = relationship('AgentTransportType', backref='AgentType', lazy=True)
    AgentTypeArchitectures = relationship('AgentTypeArchitecture', backref='AgentType', lazy=True)
    AgentTypeConfigurations = relationship('AgentTypeConfiguration', backref='AgentType', lazy=True)
    AgentTypeFormats = relationship('AgentTypeFormat', backref='AgentType', lazy=True)
    AgentTypeOperatingSystems = relationship('AgentTypeOperatingSystem', backref='AgentType', lazy=True)
    AgentTypeVersions = relationship('AgentTypeVersion', backref='AgentType', lazy=True)
    LanguageId = Column(Integer, ForeignKey('Language.Id'), nullable=False)
    Payloads = relationship('Payload', backref='AgentType', lazy=True)
    Commands = relationship('Command', backref='AgentType', lazy=True)
    Name = Column(String)
    Guid = Column(String)
    Development = Column(Boolean)

    def __repr__(self):
        return '<AgentType: %s>' % str(self.Id)
