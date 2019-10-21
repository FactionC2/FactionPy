import bcrypt
from datetime import datetime
from factionpy.backend.database import DBClient
from factionpy.models.user import User
from factionpy.processing.user_role import get_role_id
from factionpy.logger import log

db = DBClient()


def get_user(user_id='all', include_hidden=False):
    users = []
    results = []
    if user_id == 'all':
        log("get_user", "Getting all users", "debug")
        if include_hidden:
            users = db.session.query(User).all()
        else:
            users = db.session.query(User).filter_by(Visible=True)
    else:
        log("get_user", "Getting user {0}".format(user_id), "debug")
        users.append(db.session.query(User).get(user_id))
    if users:
        for user in users:
            if user.Username.lower() != 'system':
                results.append(user)
    return results


def get_user_id(username):
    user = db.session.query(User).filter_by(Username=username.lower()).first()
    if user:
        return user.Id
    else:
        return None


def create_user(username, password, role_name):
    user = User()
    user.Username = username
    user.Password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user.Created = datetime.utcnow()
    user.RoleId = get_role_id(role_name)
    user.Enabled = True
    user.Visible = True
    db.session.add(user)
    db.session.commit()
    return user

