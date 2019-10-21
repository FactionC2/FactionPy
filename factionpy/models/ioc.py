from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from factionpy.backend.database import Base


class IOC(Base):
    __tablename__ = "IOC"
    Id = Column(Integer, primary_key=True)
    Description = Column(String)
    Type = Column(String)
    Identifier = Column(String)
    Action = Column(String)
    Hash = Column(String)
    UserId = Column(Integer, ForeignKey('User.Id'))
    AgentTaskUpdateId = Column(Integer, ForeignKey('AgentTaskUpdate.Id'))
    Timestamp = Column(DateTime)

    def __repr__(self):
        return '<IOC: %s>' % str(self.Id)
