from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from factionpy.backend.database import db


class AgentTransportType(db.Base):
    __tablename__ = "AgentTransportType"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    TransportTypeGuid = Column(String)
    BuildCommand = Column(String)
    BuildLocation = Column(String)
    AgentTypeId = Column(Integer, ForeignKey('AgentType.Id'), nullable=False)
    Payloads = relationship('Payload', backref='AgentTransportType', lazy=True)

    def __repr__(self):
        return '<AgentType: %s>' % str(self.Id)
