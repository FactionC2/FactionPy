from time import sleep

import jwt
import requests
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from factionpy.config import FACTION_JWT_SECRET, GRAPHQL_ENDPOINT, QUERY_ENDPOINT, AUTH_ENDPOINT
from factionpy.files import upload_file
from factionpy.logger import log, error_out


class FactionClient:
    api_key: None
    auth_endpoint: None
    client_id: None
    retries: 20
    headers: {}

    def _request_api_key(self):
        auth_url = AUTH_ENDPOINT + "/service/"
        log(f"Authenticating to {auth_url} using JWT secret")
        key = jwt.encode({"key_name": self.client_id}, FACTION_JWT_SECRET, algorithm="HS256").decode('utf-8')
        log(f"Encoded secret: {key}", "debug")

        attempts = 1
        while self.api_key is None and attempts <= self.retries:
            try:
                r = requests.get(auth_url, headers={'Authorization': f"Bearer {key}"}, verify=False)
                if r.status_code == 200:
                    self.api_key = r.json().get("api_key")
                    self.headers = {
                        "Content-type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    }
                    return True
                else:
                    log(f"Error getting api key. Response: {r.content}", "error")
            except Exception as e:
                log(f"Failed to get API key. Attempt {attempts} of {self.retries}. Error {e}")
                attempts += 1
                sleep(3)
        return False

    def _get_type_fields(self, type_name: str):
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
        """
        Registers a webhook with Faction
        :param webhook_name: The name of your webhook (must be unique)
        :param table_name: The database table to associate the webhook with
        :param webhook_url: The URL for the webhook
        :return: {"success": bool, "message": str}
        """
        fields = self._get_type_fields(table_name)
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

    def upload_file(self, upload_type: str, file_path: str, description: str = None, agent_id: str = None,
                    source_file_path: str = None, metadata: str = None):
        """
        Uploads a file to Faction.
        :param upload_type: what type of file is being uploaded (payload, agent_upload, user_upload, etc)
        :param file_path: path to the file being uploaded
        :param description: description of the file
        :param agent_id: ID of the agent uploading the file (if agent_upload)
        :param source_file_path: Path where the file was found (if agent_upload)
        :param metadata: JSON string of metadata to be associated with the upload
        :return: {"success": bool, "message": str}
        """
        if self.api_key:
            return upload_file(upload_type=upload_type, file_path=file_path, api_key=self.api_key,
                               description=description, agent_id=agent_id, source_file_path=source_file_path,
                               metadata=metadata)
        else:
            return error_out("Could not upload file, no API key defined on client.")

    def __init__(self, client_id,
                 retries=20,
                 api_endpoint=GRAPHQL_ENDPOINT,
                 auth_endpoint=AUTH_ENDPOINT):
        self.client_id = client_id
        self.auth_endpoint = auth_endpoint
        self.api_endpoint = api_endpoint
        self.api_key = None
        self.retries = retries

        if self._request_api_key():
            api_transport = RequestsHTTPTransport(
                url=api_endpoint,
                use_json=True,
                headers=self.headers,
                verify=False
            )
            self.graphql = Client(retries=retries, transport=api_transport, fetch_schema_from_transport=True)

