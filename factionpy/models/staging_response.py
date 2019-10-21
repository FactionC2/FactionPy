from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from factionpy.backend.database import Base


class StagingResponse(Base):
    __tablename__ = "StagingResponse"
    Id = Column(Integer, primary_key=True)
    AgentId = Column(Integer, ForeignKey('Agent.Id'), nullable=False)
    StagingMessageId = Column(Integer, ForeignKey('StagingMessageId.Id'), nullable=False)
    IV = Column(String)
    HMAC = Column(String)
    Message = Column(String)
    Sent = Column(Boolean)

    def __repr__(self):
        return '<StagingResponse: %s>' % str(self.Id)
