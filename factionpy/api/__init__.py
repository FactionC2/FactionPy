import jwt
import requests
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from factionpy.config import FACTION_JWT_SECRET, GRAPHQL_ENDPOINT, QUERY_ENDPOINT, AUTH_ENDPOINT
from factionpy.logger import log


class FactionClient(Client):
    api_key: None
    auth_endpoint: None
    client_id: None

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

    def create_webhook(self, webhook_name, table_name, webhook_url):
        fields = self.get_type_fields(table_name)
        columns = []
        for field in fields:
            if field["type"]:
                columns.append(field['name'])
        key = jwt.encode({"service_name": self.client_id}, FACTION_JWT_SECRET, algorithm="HS256")
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
                   "name": "Authorization",
                   "value": "Bearer WEBHOOK_API_KEY"
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

        url = QUERY_ENDPOINT
        headers = {"Authorization": f"Bearer {self.api_key}", "content-type": "application/json"}
        r = requests.post(url, data=populated_query, headers=headers, verify=False)
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

    def request_api_key(self):
        auth_url = AUTH_ENDPOINT + "/service/"
        log("factionpy", f"Authenticating to {auth_url} using JWT secret: {FACTION_JWT_SECRET}")
        key = jwt.encode({"key_name": self.client_id}, FACTION_JWT_SECRET, algorithm="HS256").decode('utf-8')
        log("factionpy", f"Encoded secret: {key}")

        r = requests.get(auth_url, headers={'Authorization': f"Bearer {key}"}, verify=False)
        if r.status_code == 200:
            self.api_key = r.json().get("api_key")
            return True
        else:
            log("request_api_key", f"Could not get API key from {auth_url}. Response: {r.content}", "error")
            return False

    def __init__(self, client_id,
                 retries=3,
                 api_endpoint=GRAPHQL_ENDPOINT,
                 auth_endpoint=AUTH_ENDPOINT):
        self.client_id = client_id
        self.auth_endpoint = auth_endpoint
        self.api_endpoint = api_endpoint

        if self.request_api_key():
            api_transport = RequestsHTTPTransport(
                url=api_endpoint,
                use_json=True,
                headers={
                    "Content-type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                verify=False
            )
            super().__init__(retries=retries, transport=api_transport, fetch_schema_from_transport=True)

