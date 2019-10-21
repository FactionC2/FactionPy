from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from factionpy.backend.database import Base


class AgentTypeOperatingSystem(Base):
    __tablename__ = "AgentTypeOperatingSystem"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    AgentTypeId = Column(Integer, ForeignKey('AgentType.Id'), nullable=False)
    Payloads = relationship('Payload', backref='AgentTypeOperatingSystem', lazy=True)

    def __repr__(self):
        if self.Name:
            return '<AgentTypeOperatingSystem: %s>' % self.Name
        else:
            return '<AgentTypeOperatingSystem: %s>' % str(self.Id)
