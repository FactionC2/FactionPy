from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from factionpy.backend.database import Base
from factionpy.models.agent import Agent
from factionpy.models.payload import Payload


class Transport(Base):
    __tablename__ = "Transport"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    TransportType = Column(String)
    Guid = Column(String)
    Created = Column(DateTime)
    LastCheckin = Column(DateTime)
    Configuration = Column(String)
    ApiKeyId = Column(Integer, ForeignKey('ApiKey.Id'), nullable=False)
    Enabled = Column(Boolean)
    Visible = Column(Boolean)
    Agents = relationship('Agent', backref='Transport', lazy=True)
    Payloads = relationship('Payload', backref='Transport', lazy=True)

    def __repr__(self):
        return '<Transport: %s>' % str(self.Id)


