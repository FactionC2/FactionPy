from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from factionpy.backend.database import Base


class AgentTaskMessage(Base):
    __tablename__ = "AgentTaskMessage"
    Id = Column(Integer, primary_key=True)
    AgentId = Column(Integer, ForeignKey('Agent.Id'))
    AgentTaskId = Column(Integer, ForeignKey('AgentTask.Id'))
    IV = Column(String)
    HMAC = Column(String)
    Message = Column(String)
    Sent = Column(Boolean)
    Created = Column(DateTime)

    def __repr__(self):
        return '<TaskMessage: %s>' % str(self.Id)
