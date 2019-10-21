from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from factionpy.backend.database import Base
from factionpy.models.ioc import IOC


class AgentTaskUpdate(Base):
    __tablename__ = "AgentTaskUpdate"
    Id = Column(Integer, primary_key=True)
    AgentId = Column(Integer, ForeignKey('Agent.Id'))
    TaskId = Column(Integer, ForeignKey('AgentTask.Id'))
    Message = Column(String)
    Complete = Column(Boolean)
    Success = Column(Boolean)
    Received = Column(DateTime)
    IOCs = relationship("IOC", backref='AgentTaskUpdate', lazy=True)

    def __repr__(self):
        return '<AgentTaskUpdate: %s>' % str(self.Id)
