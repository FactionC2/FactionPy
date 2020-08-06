import functools

from flask import request
from factionpy.logger import log
from factionpy.services import validate_authorization_header

standard_read = [
    'admin',
    'operator',
    'read-only'
]

standard_write = [
    'admin',
    'operator'
]


def authorized_groups(groups: list):
    """
    This decorator takes a list of group names that are authorized to perform the function. The following shortcuts are
    available:
        * "standard_read" covers Admin, Operator, and Read-Only roles
        * "standard_write" covers Admin and Operator roles
        * "all" allows any authenticated user to perform the function
    These shortcuts can be combined with other group names, for example: @authorized_groups("standard_read", "transports")
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            log("factionpy:authorized_groups", "Checking if authenticated..")
            user_data = None
            authorized = False

            try:
                auth_header = request.headers.get("Authorization", None)
                if auth_header:
                    verified_header = validate_authorization_header(auth_header)
                    if verified_header["success"] == "True":
                        user_data = verified_header["results"]
            except Exception as e:
                log(f"factionpy:authorized_groups", "Could not verify Authorization header. Error: {e}")
                pass

            if user_data:
                # Replace meta group names with contents of meta group
                if 'standard_read' in groups:
                    groups.remove('standard_read')
                    groups.extend(standard_read)

                if 'standard_write' in groups:
                    groups.remove('standard_write')
                    groups.extend(standard_write)

                if 'all' in groups:
                    authorized = True

                # Iterate through valid groups, checking if the user is in there.
                if user_data['role'] in groups:
                    authorized = True

                if not authorized:
                    log("factionpy:authorized_groups",
                        "User {0} is not in the following groups: {1}".format(user_data['username'], groups))
                    pass
            return f(*args, **kwargs)
        return wrapped
    return decorator
