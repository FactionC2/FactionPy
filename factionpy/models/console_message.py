from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from factionpy.backend.database import Base


class ConsoleMessage(Base):
    __tablename__ = "ConsoleMessage"
    Id = Column(Integer, primary_key=True)
    AgentId = Column(Integer, ForeignKey('Agent.Id'), nullable=False)
    AgentTaskId = Column(Integer, ForeignKey('AgentTask.Id'), nullable=False)
    UserId = Column(Integer, ForeignKey('User.Id'), nullable=False)
    Type = Column(String)
    Content = Column(String)
    Display = Column(String)
    Received = Column(DateTime)

    def __repr__(self):
        return '<ConsoleCommand: %s>' % str(self.Id)
