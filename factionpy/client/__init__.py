from time import sleep

import jwt
import requests
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from typing import Dict, Union, Optional

from factionpy.config import FACTION_JWT_SECRET, GRAPHQL_ENDPOINT, QUERY_ENDPOINT, AUTH_ENDPOINT, VERIFY_SSL
from factionpy.files import upload_file
from factionpy.logger import log, error_out


class FactionClient:
    api_key: None
    auth_endpoint: None
    client_id: None
    retries: 20
    headers: {}

    def request_api_key(self, key_name: str) -> str:
        auth_url = AUTH_ENDPOINT + "/service/"
        log(f"Authenticating to {auth_url} using JWT secret")

        jwt_key = jwt.encode({"key_name": key_name}, FACTION_JWT_SECRET, algorithm="HS256").decode('utf-8')
        log(f"Using JWT Key: {jwt_key}", "debug")

        attempts = 1
        api_key = None
        while api_key is None and attempts <= self.retries:
            try:
                r = requests.get(auth_url, headers={'Authorization': f"Bearer {jwt_key}"}, verify=VERIFY_SSL)
                if r.status_code == 200:
                    api_key = r.json().get("api_key")
                    return api_key
                else:
                    log(f"Error getting api key. Response: {r.content}", "error")
            except Exception as e:
                log(f"Failed to get API key. Attempt {attempts} of {self.retries}. Error {e}")
                attempts += 1
                sleep(3)
        # Return an empty string if we run out of attempts
        log(f"Could not create API key within {self.retries} attempts", "error")
        return ""

    def _set_headers(self):
        self.headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

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
        result = self.graphql.execute(gquery)
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

    def create_webhook(self, webhook_name, table_name, webhook_url) -> Dict[str, Union[bool, str]]:
        """
        Registers a webhook with Faction
        :param webhook_name: The name of your webhook (must be unique)
        :param table_name: The database table to associate the webhook with
        :param webhook_url: The URL for the webhook
        :return: {"success": bool, "message": str}
        """
        webhook_api_key = self.request_api_key(webhook_name)

        if not webhook_api_key:
            return dict({
                "success": False,
                "message": "Failed to create webhook api key"
            })

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
                 "columns": "*"
               },
               "enable_manual": false,
               "update": {
                   "columns": "*"
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

        populated_query = query.replace("WEBHOOK_NAME", webhook_name)
        populated_query = populated_query.replace("TABLE_NAME", table_name)
        populated_query = populated_query.replace("WEBHOOK_URL", webhook_url)
        populated_query = populated_query.replace("WEBHOOK_API_KEY", webhook_api_key)

        url = QUERY_ENDPOINT
        headers = {"Authorization": f"Bearer {self.api_key}", "content-type": "application/json"}
        r = requests.post(url, data=populated_query, headers=headers, verify=VERIFY_SSL)
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
                    source_file_path: str = None, metadata: str = None) -> Dict[str, Union[str, bool]]:
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
        self.retries = retries
        self.api_key = self.request_api_key(client_id)

        if self.api_key:
            self._set_headers()
            api_transport = RequestsHTTPTransport(
                url=api_endpoint,
                use_json=True,
                headers=self.headers,
                verify=VERIFY_SSL
            )
            self.graphql = Client(retries=retries, transport=api_transport, fetch_schema_from_transport=True)
        else:
            log(f"Could not get API key for Faction client.", "error")
