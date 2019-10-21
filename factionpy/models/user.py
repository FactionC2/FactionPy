import bcrypt
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import relationship

from factionpy.logger import log
from factionpy.backend.database import Base, DBClient
from factionpy.models.api_key import ApiKey
from factionpy.models.console_message import ConsoleMessage
from factionpy.models.faction_file import FactionFile

db = DBClient


class User(Base):
    __tablename__ = "User"
    Id = Column(Integer, primary_key=True)
    Username = Column(String, unique=True)
    Password = Column(LargeBinary)
    RoleId = Column(Integer, ForeignKey('UserRole.Id'), nullable=False)
    ApiKeys = relationship("ApiKey", backref='User', lazy=True)
    Authenticated = Column(Boolean, default=False)
    ConsoleMessages = relationship("ConsoleMessage", backref='User', lazy=True)
    Files = relationship("FactionFile", backref='User', lazy=True)
    Created = Column(DateTime)
    LastLogin = Column(DateTime)
    Enabled = Column(Boolean)
    Visible = Column(Boolean)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.Username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.Authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def change_password(self, current_password, new_password):
        log("change_password", "Got password change request", "debug")
        if bcrypt.checkpw(current_password.encode('utf-8'), self.Password) and self.Enabled:
            self.Password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            db.session.add(self)
            db.session.commit()
            log("change_password", "Password changed", "debug")
            return dict({
                "Success": True,
                "Message": 'Changed password for user: {0}'.format(self.Username)
            })
        log("change_password", "Current password incorrect", "debug")
        return {
            'Success': False,
            'Message': 'Invalid username or password.'
        }

    def get_api_keys(self):
        api_keys = self.ApiKeys
        log("get_api_keys", "Got api keys: {0}".format(str(api_keys)), "debug")
        results = []
        for api_key in api_keys:
            result = dict()
            result['Id'] = api_key.Id
            result['Name'] = api_key.Name
            result['Created'] = None
            result['LastUsed'] = None
            result['Type'] = api_key.Type
            if api_key.Created:
                result['Created'] = api_key.Created.isoformat()
            if api_key.LastUsed:
                result['LastUsed'] = api_key.LastUsed.isoformat()
            results.append(result)
        return {
            'Success': True,
            'Results': results
        }

    def delete_api_key(self, api_key_id):
        api_keys = self.ApiKeys
        for api_key in api_keys:
            if api_key.Id == api_key_id:
                db.session.delete(api_key)
                db.session.commit()
                return {
                    'Success': True,
                    'Message': "Api Key {0} deleted".format(api_key.Name)
                }
        return {
            'Success': False,
            'Message': "Api Key ID: {0} not found".format(api_key_id)
        }
