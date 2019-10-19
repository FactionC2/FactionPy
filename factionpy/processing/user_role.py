import functools
from flask_login import current_user
from backend.database import db
from models.user_role import UserRole
from logger import log

standard_read = [
    'Admin',
    'Operator',
    'ReadOnly'
]

standard_write = [
    'Admin',
    'Operator'
]

# When one of these groups is specified, we substitute them for the 'system' group. This adds an extra check
# to make sure system api keys aren't used for anything weird. Its also the only way I could figure out how
# to make it work in the first place.
system_groups = [
    'Transport',
    'FileUpload'
]


def create_role(name):
    role = UserRole()
    role.Name = name.lower()
    db.session.add(role)
    db.session.commit()


def get_role(role_id='all'):
    results = []
    log("get_role", "Getting role for id: {0}".format(role_id))
    if role_id == 'all':
        roles = UserRole.query.all()
    else:
        roles = UserRole.query.get(role_id)
    for role in roles:
        if role.Name.lower() != 'system':
            results.append(role)
    return results


def get_role_id(name):
    log("get_role_id", "Getting role {0}".format(name))
    role = UserRole.query.filter_by(Name=name.lower()).first()
    if role:
        log("get_role_id", "Got role {0}".format(role.Id))
        return role.Id
    else:
        log("get_role_id", "Role not found")
        return None


def get_role_name(role_id):
    log("get_role_name", "Getting role name {0}".format(role_id))
    role = UserRole.query.get(role_id)
    if role:
        log("get_role_name", "Got role name {0}".format(role.Name))
        return role.Name
    else:
        log("get_role_name", "Role not found")
        return None
