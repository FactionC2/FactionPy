from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, LargeBinary, String

from factionpy.backend.database import Base


class ApiKey(Base):
    __tablename__ = "ApiKey"
    Id = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey('User.Id'))
    OwnerId = Column(Integer)
    TransportId = Column(Integer, ForeignKey('Transport.Id'))
    Name = Column(String, unique=True)
    Type = Column(String)
    Key = Column(LargeBinary)
    Created = Column(DateTime)
    LastUsed = Column(DateTime)
    Enabled = Column(Boolean)
    Visible = Column(Boolean)

    def __repr__(self):
        return '<ApiKey: %s>' % str(self.Id)
