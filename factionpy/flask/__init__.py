from flask import request, jsonify
from factionpy.logger import log
from functools import wraps
from factionpy.services import validate_authorization_header

standard_read = [
    'super-user',
    'user',
    'read-only'
]

standard_write = [
    'super-user',
    'user'
]


class authorized_groups(object):
    def __init__(self, groups: list):
        self.groups = groups

    def __call__(self, func):

        @wraps(func)
        def callable(*args, **kwargs):
            log(f"Checking if authenticated..", "debug")
            user_data = None
            groups = self.groups
            try:
                auth_header = request.headers.get("Authorization", None)
                if auth_header:
                    log(f"got auth_header", "debug")
                    verified_header = validate_authorization_header(auth_header)
                    if verified_header["success"] == "true":
                        log(f"got verified_header: {verified_header}", "debug")
                        user_data = verified_header["result"]
                        log(f"returning user_data: {user_data}", "debug")
            except Exception as e:
                log(f"Could not verify Authorization header. Error: {e}", "error")
                return jsonify({
                    "success": "false",
                    "message": f"Could not verify Authorization header. Error: {e}"
                }), 401

            if user_data:
                try:
                    log(f"got user_data: {user_data}", "debug")
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
                        log(f"user authorized. returning results of function.", "debug")
                        return func(*args, **kwargs)
                    else:
                        log(f"User {user_data['username']} is not in the following groups: {groups}")
                except Exception as e:
                    log(f"Could not verify user_data. Error: {e}", "error")
                    pass
            return jsonify({
                "success": "false",
                "message": f"Invalid API key provided or you do not have permission to perform this action."
            }), 401

        return callable
