from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from factionpy.config import get_config_value

api_transport = RequestsHTTPTransport(
    url=get_config_value("API_ENDPOINT"),
    use_json=True,
    headers={
        "Content-type": "application/json",
        "x-hasura-admin-secret": "admin"
    },
    verify=False
)

client = Client(
    retries=3,
    transport=api_transport,
    fetch_schema_from_transport=True,
)
