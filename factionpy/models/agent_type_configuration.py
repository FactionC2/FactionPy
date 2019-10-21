from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from factionpy.backend.database import Base


class AgentTypeConfiguration(Base):
    __tablename__ = "AgentTypeConfiguration"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    AgentTypeId = Column(Integer, ForeignKey('AgentType.Id'), nullable=False)
    Payloads = relationship('Payload', backref='AgentTypeConfiguration', lazy=True)

    def __repr__(self):
        if self.Name:
            return '<AgentTypeConfiguration: %s>' % self.Name
        else:
            return '<AgentTypeConfiguration: %s>' % str(self.Id)
