from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from factionpy.backend.database import Base


class AgentTypeArchitecture(Base):
    __tablename__ = "AgentTypeArchitecture"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    AgentTypeId = Column(Integer, ForeignKey('AgentType.Id'), nullable=False)
    Payloads = relationship('Payload', backref='AgentTypeArchitecture', lazy=True)

    def __repr__(self):
        if self.Name:
            return '<AgentTypeArchitecture: %s>' % self.Name
        else:
            return '<AgentTypeArchitecture: %s>' % str(self.Id)
