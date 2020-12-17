import datetime
import json
from typing import Dict

import dateutil.parser
import requests

from factionpy.config import AUTH_ENDPOINT, VERIFY_SSL
from factionpy.logger import log


class HasuraRequest:
    """
    An object representing the JSON that Hasura sends to a webhook.

    Args:
        body (str): The JSON string that Hasura sent for this operation

    Attributes:
        id (str): The request ID
        trigger_name (str): The name of the trigger that generated the request
        table_name (str): The table that the request is associated with
        table_schema (str): The schema of the table that the request is associated with
        created_at (datetime): When the request was generated
        operation (str): What type of operation was performed (INSERT, UPDATE, DELETE)
        session_variables (Dict[str, object]): Session variables associated with the request (X-Hasura-Role, etc)
        old_data (Dict[str, object]): The original data (if INSERT, this is null)
        new_data (Dict[str, object]): The new data
    """
    id: str = None
    trigger_name: str = None
    table_name: str = None
    table_schema: str = None
    created_at: datetime = None
    operation: str = None
    session_variables: Dict[str, object] = None
    old_data: Dict[str, object] = None
    new_data: Dict[str, object] = None

    def __init__(self, hasura_json: dict):
        """
        :param hasura_json: Dictionary representing that JSON string that Hasura sent for this operation
        """
        self.id = hasura_json['id']
        self.trigger_name = hasura_json['trigger']['name']
        self.table_name = hasura_json['table']['name']
        self.table_schema = hasura_json['table']['schema']
        self.created_at = dateutil.parser.parse(hasura_json['created_at'])
        self.operation = hasura_json['event']['op']
        self.session_variables = hasura_json['event']['session_variables']
        self.old_data = hasura_json['event']['data']['old']
        self.new_data = hasura_json['event']['data']['new']


def validate_authorization_header(header_value: str) -> Dict[str, str]:
    """
    :param header_value: The value of the Authorization heard to be verified
    :param verify_ssl: Whether to require a valid SSL cert on the Authentication endpoint or not
    :return: {"success": "<true|false>", "result": "<response from authentication endpoint>"}
    """
    log(f"got header {header_value}", "debug")
    success = "false"
    result = None
    try:
        headers = {"Authorization": header_value}
        url = f"{AUTH_ENDPOINT}/verify/"
        log(f"using url: {url}", "debug")
        r = requests.get(url, headers=headers, verify=VERIFY_SSL).json()
        log(f"got response {r}", "debug")
        if r['success'] == "true":
            success = "true"
            result = r
    except Exception as e:
        result = e
    rsp = {"success": success, "result": result}
    log(f"returning: {rsp}", "debug")
    return rsp
