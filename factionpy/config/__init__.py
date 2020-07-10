from factionpy.kubernetes import get_secret, get_ingress_host

HOST = get_ingress_host()
QUERY_ENDPOINT = f"https://{HOST}/api/v1/query"
GRAPHQL_ENDPOINT = f"https://{HOST}/api/v1/graphql"
AUTH_ENDPOINT = f"https://{HOST}/api/v1/auth"
FACTION_JWT_SECRET = get_secret("auth-secrets", "jwt-secret")


