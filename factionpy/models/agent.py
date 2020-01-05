from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import backref, relationship

from factionpy.backend.database import Base

from factionpy.models.module import Module
from factionpy.models.agent_task import AgentTask
from factionpy.models.console_message import ConsoleMessage


AgentsTransportsXREF = Table('AgentsTransportsXREF',
                             Base.metadata,
                             Column('AgentId', Integer, ForeignKey('Agent.Id'), primary_key=True),
                             Column('TransportId', Integer, ForeignKey('Transport.Id'), primary_key=True)
                             )

AgentModulesXREF = Table('AgentModulesXREF',
                         Base.metadata,
                         Column('AgentId', Integer, ForeignKey('Agent.Id'), primary_key=True),
                         Column('ModuleId', Integer, ForeignKey('Module.Id'), primary_key=True)
                         )


class Agent(Base):
    __tablename__ = "Agent"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    StagingId = Column(String)
    AesPassword = Column(String)
    Username = Column(String)
    Hostname = Column(String)
    PID = Column(Integer)
    OperatingSystem = Column(String)
    Admin = Column(Boolean)
    AgentTypeId = Column(Integer, ForeignKey('AgentType.Id'), nullable=False)
    StagingResponseId = Column(Integer, ForeignKey('StagingMessage.Id'), nullable=False)
    PayloadId = Column(Integer, ForeignKey('Payload.Id'), nullable=False)
    TransportId = Column(Integer, ForeignKey('Transport.Id'), nullable=False)
    InternalIP = Column(String)
    ExternalIP = Column(String)
    InitialCheckin = Column(DateTime)
    LastCheckin = Column(DateTime)
    BeaconInterval = Column(Integer)
    Jitter = Column(Float)
    Tasks = relationship('AgentTask', backref='Agent', lazy=True)
    ConsoleMessages = relationship("ConsoleMessage", backref='Agent', lazy=True)
    AvailableTransports = relationship('Transport', secondary=AgentsTransportsXREF, lazy='subquery',
                                       backref=backref('AvailableAgents', lazy=True))
    AvailableModules = relationship('Module', secondary=AgentModulesXREF, lazy='subquery',
                                    backref=backref('AvailableAgents', lazy=True))
    Visible = Column(Boolean)

    def __repr__(self):
        if self.Name:
            return '<Agent: %s>' % self.Name
        else:
            return '<Agent: %s>' % str(self.Id)
