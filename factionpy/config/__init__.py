import os
from factionpy.kubernetes import CONNECTED_TO_KUBERNETES, get_secret, get_ingress_host


if CONNECTED_TO_KUBERNETES:
    HOST = get_ingress_host()
    QUERY_ENDPOINT = f"https://{HOST}/api/v1/query"
    GRAPHQL_ENDPOINT = f"https://{HOST}/api/v1/graphql"
    AUTH_ENDPOINT = f"https://{HOST}/api/v1/auth"
    FACTION_JWT_SECRET = get_secret("auth-secrets", "jwt-secret")
else:
    QUERY_ENDPOINT = f"http://faction-hasura:8080/api/v1/query"
    GRAPHQL_ENDPOINT = f"http://faction-hasura:8080/api/v1/graphql"
    AUTH_ENDPOINT = f"http://faction-auth"
    FACTION_JWT_SECRET = os.environ.get("FACTION_JWT_SECRET", None)

