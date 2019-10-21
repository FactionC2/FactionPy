from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from factionpy.backend.database import Base


class StagingMessage(Base):
    __tablename__ = "StagingMessage"
    Id = Column(Integer, primary_key=True)
    AgentName = Column(String)
    SourceIp = Column(String)
    PayloadName = Column(String)
    PayloadId = Column(Integer, ForeignKey('Payload.Id'), nullable=False)
    TransportId = Column(Integer, ForeignKey('Transport.Id'), nullable=False)
    StagingId = Column(String)
    IV = Column(String)
    HMAC = Column(String)
    Message = Column(String)
    Received = Column(DateTime)

    def __repr__(self):
        return '<StagingMessage: %s>' % str(self.Id)
