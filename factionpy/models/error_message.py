from sqlalchemy import Column, DateTime, Integer, String

from factionpy.backend.database import Base


class ErrorMessage(Base):
    __tablename__ = "ErrorMessage"
    Id = Column(Integer, primary_key=True)
    Source = Column(String)
    Message = Column(String)
    Details = Column(String)
    Timestamp = Column(DateTime)

    def __repr__(self):
        return '<ErrorMessage: {0} - {1}>'.format(self.Source, self.Message)
