import os
from distutils.util import strtobool
from factionpy.kubernetes import CONNECTED_TO_KUBERNETES, get_secret, get_ingress_host
from factionpy.logger import log


HOST = None

if CONNECTED_TO_KUBERNETES:
    log(f"Pulling config from Kubernetes")
    HOST = get_ingress_host()
    QUERY_ENDPOINT = f"https://{HOST}/api/v1/query"
    GRAPHQL_ENDPOINT = f"https://{HOST}/api/v1/graphql"
    AUTH_ENDPOINT = f"https://{HOST}/api/v1/auth"
    FILES_ENDPOINT = f"https://{HOST}/api/v1/files"
    FACTION_JWT_SECRET = get_secret("auth-secrets", "jwt-secret")
else:
    log(f"Using hardcoded config")
    QUERY_ENDPOINT = f"http://faction-hasura:8080/v1/query"
    GRAPHQL_ENDPOINT = f"http://faction-hasura:8080/v1/graphql"
    AUTH_ENDPOINT = f"http://faction-auth:5000"
    FILES_ENDPOINT = f"http://faction-files:5000/"
    FACTION_JWT_SECRET = os.environ.get("FACTION_JWT_SECRET", None)

VERIFY_SSL = bool(strtobool(os.environ.get("FACTION_VERIFY_SSL", "True")))

log(f"config value QUERY_ENDPOINT:\t {QUERY_ENDPOINT}", "debug")
log(f"config value GRAPHQL_ENDPOINT:\t {GRAPHQL_ENDPOINT}", "debug")
log(f"config value AUTH_ENDPOINT:\t {AUTH_ENDPOINT}", "debug")
log(f"config value FILES_ENDPOINT:\t {FILES_ENDPOINT}", "debug")
log(f"config value FACTION_JWT_SECRET:\t {FACTION_JWT_SECRET}", "debug")
log(f"config value VERIFY_SSL:\t {VERIFY_SSL}", "debug")
