from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from factionpy.backend.database import Base


class AgentCheckin(Base):
    __tablename__ = "AgentCheckin"
    Id = Column(Integer, primary_key=True)
    AgentId = Column(Integer, ForeignKey('Agent.Id'))
    IV = Column(String)
    HMAC = Column(String)
    Message = Column(String)
    Received = Column(DateTime)

    def __repr__(self):
        return '<AgentCheckin: %s>' % str(self.Id)
