import bcrypt
from datetime import datetime
from backend.database import db
from models.user import User
from processing.user_role import get_role_id
from logger import log


def get_user(user_id='all', include_hidden=False):
    users = []
    results = []
    if user_id == 'all':
        log("get_user", "Getting all users")
        if include_hidden:
            users = User.query.all()
        else:
            users = User.query.filter_by(Visible=True)
    else:
        log("get_user", "Getting user {0}".format(user_id))
        users.append(User.query.get(user_id))
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
    print(user.RoleId)
    print('Creating user %s ' % user.Username)
    db.session.add(user)
    db.session.commit()
    return user

