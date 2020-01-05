from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from factionpy.backend.database import Base
from factionpy.models.agent import Agent
from factionpy.models.staging_message import StagingMessage


class Payload(Base):
    __tablename__ = "Payload"
    Id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)
    Description = Column(String)
    Key = Column(String)

    Built = Column(Boolean)
    BuildToken = Column(String)
    Filename = Column(String)

    Agents = relationship('Agent', backref='Payload', lazy=True)
    AgentTypeId = Column(Integer, ForeignKey('AgentType.Id'), nullable=False)
    AgentTypeArchitectureId = Column(Integer, ForeignKey('AgentTypeArchitecture.Id'), nullable=False)
    AgentTypeConfigurationId = Column(Integer, ForeignKey('AgentTypeConfiguration.Id'), nullable=False)
    AgentTypeOperatingSystemId = Column(Integer, ForeignKey('AgentTypeOperatingSystem.Id'), nullable=False)
    AgentTypeVersionId = Column(Integer, ForeignKey('AgentTypeVersion.Id'), nullable=False)
    AgentTypeFormatId = Column(Integer, ForeignKey('AgentTypeFormat.Id'), nullable=False)
    AgentTransportTypeId = Column(Integer, ForeignKey('AgentTransportType.Id'), nullable=False)
    TransportId = Column(Integer, ForeignKey('Transport.Id'), nullable=False)

    BeaconInterval = Column(Integer)
    Jitter = Column(Float)
    Created = Column(DateTime)
    LastDownloaded = Column(DateTime)
    ExpirationDate = Column(DateTime)
    Enabled = Column(Boolean)

    Agents = relationship('Agent', backref='Payload', lazy=True)
    StagingMessages = relationship("StagingMessage", backref='StagingConfig', lazy=True)
    Visible = Column(Boolean)

    def __repr__(self):
        return '<Payload: %s>' % str(self.Id)
