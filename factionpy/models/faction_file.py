from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from factionpy.backend.database import Base


class FactionFile(Base):
    __tablename__ = "FactionFile"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    Hash = Column(String)
    HashMatch = Column(Boolean)
    UserId = Column(Integer, ForeignKey('User.Id'))
    AgentId = Column(Integer, ForeignKey('Agent.Id'))
    Created = Column(DateTime)
    LastDownloaded = Column(DateTime)
    Visible = Column(Boolean)

    def __repr__(self):
        return '<FactionFile: %s>' % str(self.Id)
