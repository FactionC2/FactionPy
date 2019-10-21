import functools
from factionpy.backend.database import DBClient
from factionpy.models.user_role import UserRole
from factionpy.logger import log

db = DBClient()

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
    log("get_role", "Getting role for id: {0}".format(role_id), "debug")
    if role_id == 'all':
        roles = db.session.query(UserRole).all()
    else:
        roles = db.session.query(UserRole).get(role_id)
    for role in roles:
        if role.Name.lower() != 'system':
            results.append(role)
    return results


def get_role_id(name):
    log("get_role_id", "Getting role {0}".format(name), "debug")
    role = db.session.query(UserRole).filter_by(Name=name.lower()).first()
    if role:
        log("get_role_id", "Got role {0}".format(role.Id), "debug")
        return role.Id
    else:
        log("get_role_id", "Role not found", "debug")
        return None


def get_role_name(role_id):
    log("get_role_name", "Getting role name {0}".format(role_id), "debug")
    role = db.session.query(UserRole).get(role_id)
    if role:
        log("get_role_name", "Got role name {0}".format(role.Name), "debug")
        return role.Name
    else:
        log("get_role_name", "Role not found", "debug")
        return None
