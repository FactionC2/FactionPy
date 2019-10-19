from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from factionpy.backend.database import db
from factionpy.models.user import User


class UserRole(db.Base):
    __tablename__ = "UserRole"
    Id = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False, unique=True)
    Users = relationship('User', backref='UserRole', lazy=True)

    def __repr__(self):
        return '<Role: %s>' % str(self.Id)
