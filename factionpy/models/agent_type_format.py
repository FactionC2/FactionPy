from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from factionpy.backend.database import Base


class AgentTypeFormat(Base):
    __tablename__ = "AgentTypeFormat"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    AgentTypeId = Column(Integer, ForeignKey('AgentType.Id'), nullable=False)
    Payloads = relationship('Payload', backref='AgentTypeFormat', lazy=True)

    def __repr__(self):
        if self.Name:
            return '<AgentTypeFormat: %s>' % self.Name
        else:
            return '<AgentTypeFormat: %s>' % str(self.Id)
