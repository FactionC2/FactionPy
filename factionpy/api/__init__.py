import jwt
import requests
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from factionpy.config import get_config_value
from factionpy.logger import log


class FactionClient(Client):
    api_key: None
    auth_endpoint: None
    service_name: None

    def get_type_fields(self, type_name):
        query = '''query MyQuery {
__type(name: "TYPENAME") {
  fields {
    name
      type{
        name
        kind
        ofType{
          name
          kind
        }
      }
    }
  }
}'''.replace("TYPENAME", type_name)
        log("FactionClient.get_type_fields", query)
        gquery = gql(query)
        result = self.execute(gquery)
        results = []
        for item in result["__type"]["fields"]:
            name = item['name']
            item_type = item['type']['name']
            if not item_type:
                try:
                    if item['type']['ofType']['kind'] == 'SCALAR':
                        item_type = item['type']['ofType']['name']
                except:
                    item_type = None
            results.append(dict({
                "name": name,
                "type": item_type
            }))
        return results

    def create_webhook(self, webhook_name, table_name, webhook_url, jwt_secret=None):
        if not jwt_secret:
            jwt_secret = get_config_value("FACTION_SERVICE_SECRET")
        fields = self.get_type_fields(table_name)
        columns = []
        for field in fields:
            if field["type"]:
                columns.append(field['name'])
        key = jwt.encode({"service_name": self.service_name}, jwt_secret, algorithm="HS256")
        webhook_api_key = key
        query = '''{
             "type": "create_event_trigger",
             "args": {
               "name": "WEBHOOK_NAME",
               "table": {
                "name": "TABLE_NAME",
                 "schema": "public"
               },
              "webhook": "WEBHOOK_URL",
               "insert": {
                 "columns": COLUMNS
               },
               "enable_manual": false,
               "update": {
                   "columns": COLUMNS
                  },
               "retry_conf": {
                 "num_retries": 10,
                 "interval_sec": 10,
                 "timeout_sec": 60
               },
               "headers": [
                 {
                   "name": "X-Faction-API-Key",
                   "value": "WEBHOOK_API_KEY"
                 }
               ]
             }
           }'''

        populated_query = query\
            .replace("WEBHOOK_NAME", webhook_name)\
            .replace("TABLE_NAME", table_name)\
            .replace("WEBHOOK_URL", webhook_url)\
            .replace("WEBHOOK_API_KEY", webhook_api_key)\
            .replace("COLUMNS", str(columns).replace("'", '"'))

        url = get_config_value("QUERY_ENDPOINT")
        headers = {"X-Faction-API-Key": self.api_key, "content-type": "application/json"}
        r = requests.post(url, data=populated_query, headers=headers)
        if r.status_code == 200:
            return dict({
                "success": True,
                "message": "Successfully created webhook"
            })
        else:
            return dict({
                "success": False,
                "Message": r.content
            })

    def request_api_key(self, secret=None, auth_endpoint=None):
        if not secret:
            secret = get_config_value("FACTION_SERVICE_SECRET")
        if not auth_endpoint:
            auth_endpoint = get_config_value("AUTH_ENDPOINT")
        auth_url = auth_endpoint + "/auth/service/"
        key = jwt.encode({"service_name": self.service_name}, secret, algorithm="HS256")
        r = requests.get(auth_url, headers={'X-Faction-Service-Auth': key})
        if r.status_code == 200:
            self.api_key = r.json().get("api_key")
            return True
        return False

    def __init__(self, service_name,
                 retries=3,
                 api_endpoint=get_config_value("GRAPHQL_ENDPOINT"),
                 auth_endpoint=get_config_value("AUTH_ENDPOINT")):

        if self.request_api_key(auth_endpoint=auth_endpoint):
            api_transport = RequestsHTTPTransport(
                url=api_endpoint,
                use_json=True,
                headers={
                    "Content-type": "application/json",
                    "X-Faction-API-Key": self.api_key
                },
                verify=False
            )
            super().__init__(retries=retries, transport=api_transport, fetch_schema_from_transport=True)
            self.service_name = service_name
            self.auth_endpoint = auth_endpoint
        else:
            print(f"Could not get API key for Faction from: {auth_endpoint}")

