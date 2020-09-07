from functools import wraps

from flask import _request_ctx_stack, has_request_context, current_app
from werkzeug.local import LocalProxy

from factionpy.logger import log

standard_read = [
    'admin',
    'super-user',
    'service',
    'user',
    'read-only'
]

standard_write = [
    'admin',
    'super-user',
    'service',
    'user'
]


current_user = LocalProxy(lambda: _get_user())


def _get_user():
    log(f"Called", "debug")
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        log(f"Running _load_user()", "debug")
        current_app.faction._load_user()
    return getattr(_request_ctx_stack.top, 'user', None)


class authorized_groups(object):
    def __init__(self, groups: list):
        self.groups = groups

    def __call__(self, func):
        @wraps(func)
        def callable(*args, **kwargs):
            log(f"Current user: {current_user.username}")
            groups = self.groups
            authorized = False

            if current_user.enabled:
                try:
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
                    if current_user.role in groups:
                        authorized = True
                    else:
                        log(f"User {current_user.username} is not in the following groups: {groups}")
                except Exception as e:
                    log(f"Could not verify user_data. Error: {e}", "error")
                    pass
                if authorized:
                    try:
                        log(f"user authorized. returning results of function.", "debug")
                        return func(*args, **kwargs)
                    except Exception as e:
                        log(f"Error executing function: {e}", "error")
                        pass
            return {
                "success": "false",
                "message": f"Invalid API key provided or you do not have permission to perform this action."
            }, 401

        return callable