from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from factionpy.backend.database import Base
from factionpy.models.agent_task_update import AgentTaskUpdate


# Even though the API doesn't handle tasks (Core does that), we need to define this model
# so we can have an agent object thats inline with the DB
class AgentTask(Base):
    __tablename__ = "AgentTask"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    AgentId = Column(Integer, ForeignKey('Agent.Id'), nullable=False)
    ConsoleMessageId = Column(Integer, ForeignKey('ConsoleMessage.Id'), nullable=True)
    AgentTaskUpdates = relationship('AgentTaskUpdate', backref='AgentTask', lazy=True)
    Action = Column(String)
    Command = Column(String)
    Created = Column(DateTime)

    def __repr__(self):
        return '<Task: %s>' % str(self.Id)
