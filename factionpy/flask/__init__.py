import os
from time import sleep

from flask import request, has_request_context, _request_ctx_stack

from factionpy.logger import log, error_out
from factionpy.client import FactionClient
from factionpy.services import validate_authorization_header
from factionpy.config import QUERY_ENDPOINT, GRAPHQL_ENDPOINT, AUTH_ENDPOINT, FACTION_JWT_SECRET


class FactionApp(object):
    def __init__(self, app_name: str, app: object, retries=5):
        """
        Creates a Faction app for Flask.
        :param app_name: The name of your application. This is used for tracking API authentication requests
        :param app: Your Flask app object
        :param retries: The number of times to attempt to create a Faction client. Default is 5.
        """
        self.current_user = User()
        self.client = None

        attempts = 1
        while self.client is None and attempts <= retries:
            try:
                self.client = FactionClient.create(app_name)
            except Exception as e:
                log(f"Error creating faction client. Attempt {attempts} of {retries}. Error: {e}")
                attempts += 1
                sleep(3)

        if self.client is None:
            log(f"Could not create Faction client", "error")

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.faction = self
        app.config.setdefault('FACTION_QUERY_ENDPOINT', QUERY_ENDPOINT)
        app.config.setdefault('FACTION_GRAPHQL_ENDPOINT', GRAPHQL_ENDPOINT)
        app.config.setdefault('FACTION_AUTH_ENDPOINT', AUTH_ENDPOINT)
        app.config.setdefault('FACTION_JWT_SECRET', FACTION_JWT_SECRET)

    def _load_user(self):
        """
        This populates the User value of the request context. It first creates a default user object for an anonymous
        user (enabled set to false). It then tries to authenticate the request from its API key. If the API key returns
        a valid user, the anonymous user details are updated to that of the authenticated user.
        """
        log(f"Checking if authenticated..", "debug")
        user = User()

        try:
            auth_header = request.headers.get("Authorization", None)
            if auth_header:
                log(f"got auth_header", "debug")
                verified_header = validate_authorization_header(auth_header)
                if verified_header["success"] == "true":
                    log(f"got verified_header: {verified_header}", "debug")
                    user_data = verified_header["result"]
                    user.id = user_data["id"]
                    user.username = user_data["username"]
                    user.role = user_data["role"]
                    user.last_login = user_data["last_login"]
                    user.created = user_data["created"]
                    user.enabled = user_data["enabled"]
                    user.visible = user_data["visible"]
                    user.api_key_name = user_data["api_key"]
                    user.api_key_description = user_data["api_key_description"]
                    log(f"returning user_data: {user_data}", "debug")
        except Exception as e:
            log(f"Could not verify Authorization header. Error: {e}", "error")
        ctx = _request_ctx_stack.top
        ctx.user = user


class User(object):
    id = None
    username = None
    role = None
    last_login = None
    created = None
    enabled = False
    visible = False
    api_key_name = None
    api_key_description = None

    def __init__(self,
                 id: str = None,
                 username: str = None,
                 role: str = None,
                 last_login: str = None,
                 created: str = None,
                 enabled: bool = False,
                 visible: bool = False):
        self.id = id
        self.username = username
        self.role = role
        self.last_login = last_login
        self.created = created
        self.enabled = enabled
        self.visible: visible
