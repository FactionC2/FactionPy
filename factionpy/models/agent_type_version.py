from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from factionpy.backend.database import Base


class AgentTypeVersion(Base):
    __tablename__ = "AgentTypeVersion"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    AgentTypeId = Column(Integer, ForeignKey('AgentType.Id'), nullable=False)
    Payloads = relationship('Payload', backref='AgentTypeVersion', lazy=True)

    def __repr__(self):
        if self.Name:
            return '<AgentTypeVersion: %s>' % self.Name
        else:
            return '<AgentTypeVersion: %s>' % str(self.Id)
