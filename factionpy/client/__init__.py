from pathlib import Path
from time import sleep
from uuid import UUID

import jwt
import httpx
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from typing import Dict, Union, Optional

from factionpy.config import FACTION_JWT_SECRET, GRAPHQL_ENDPOINT, QUERY_ENDPOINT, AUTH_ENDPOINT, VERIFY_SSL
from factionpy.files import FileProperties, upload_file
from factionpy.logger import log, error_out

http = httpx.AsyncClient(verify=VERIFY_SSL)


class FactionClient:
    api_key: None
    auth_endpoint: None
    client_id: None
    retries: 20
    headers: {}

    def request_api_key(self, key_name: str) -> Optional[str]:
        auth_url = AUTH_ENDPOINT + "/service/"
        log(f"Authenticating to {auth_url} using JWT secret")

        jwt_key = jwt.encode({"key_name": key_name}, FACTION_JWT_SECRET, algorithm="HS256")
        log(f"Using JWT Key: {jwt_key}", "debug")

        attempts = 1
        api_key = None
        while api_key is None and attempts <= self.retries:
            try:
                r = httpx.get(auth_url, headers={'Authorization': f"Bearer {jwt_key}"}, verify=VERIFY_SSL)
                if r.status_code == 200:
                    api_key = r.json().get("access_key")
                    if api_key:
                        api_key_name, api_key_value = api_key.split('.', 1)
                        log(f"Got API key named: {api_key_name}", "debug")
                        return api_key
                    else:
                        log(f"Received empty or invalid API key.", "error")
                else:
                    log(f"Error getting api key. Response: {r.content}", "error")
            except Exception as e:
                log(f"Failed to get API key. Attempt {attempts} of {self.retries}. Error {e}")
                attempts += 1
                sleep(3)
        # Return an empty string if we run out of attempts
        log(f"Could not create API key within {self.retries} attempts", "error")
        return None

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

    async def create_webhook(self, webhook_name, table_name, webhook_url) -> Dict[str, Union[bool, str]]:
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

        query = {
            "type": "create_event_trigger",
            "args": {
                "name": webhook_name,
                "table": {
                    "name": table_name,
                    "schema": "public"
                },
                "webhook": webhook_url,
                "insert": {
                    "columns": "*"
                },
                "enable_manual": False,
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
                        "value": f"Bearer {webhook_api_key}"
                    }
                ]
            }
        }

        url = QUERY_ENDPOINT
        headers = {"Authorization": f"Bearer {self.api_key}", "content-type": "application/json"}
        r = await http.post(url, data=query, headers=headers)
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

    async def get_file_by_id(self, file_id: UUID) -> Optional[FileProperties]:
        get_file_by_id_query = f"""
    query get_file_by_id {{
      files(where: {{id: {{_eq: "{file_id}"}}}}) {{
        id
        description
        type
        file_path
        agent_id
        source_file_path
        user_id
        created
        last_downloaded
        enabled
        url
        metadata
      }}
    }}
    """
        log(f"executing query: {get_file_by_id_query}")
        try:
            result = await self.graphql.execute(gql(get_file_by_id_query))
            if result:
                file_info = FileProperties.parse_obj(result["files"][0])
                return file_info
        except Exception as e:
            log(f"Could not find file with id {file_id}: Error: {e}", "error")
        return None

    async def upload_file(self, file_path: Path, file_properties: FileProperties) -> Dict[str, Union[str, bool]]:
        """
        Uploads a file to Faction.
        :param file_path:
        :param file_properties:
        """
        if self.api_key:
            return await upload_file(api_key=self.api_key, file_path=file_path, file_properties=file_properties)
        else:
            return error_out("Could not upload file, no API key defined on client.")

    def __init__(self,
                 client_id,
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
                verify=VERIFY_SSL,
                retries=retries
            )
            self.graphql = Client(transport=api_transport, fetch_schema_from_transport=True)
        else:
            raise AttributeError(f"Could not get API key for Faction client.")

