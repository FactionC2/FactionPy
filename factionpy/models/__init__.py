import datetime
import dateutil.parser
from enum import Enum
from uuid import UUID
from typing import Optional, Dict, Any

import dateutil
from pydantic import BaseModel


class ApiKey(BaseModel):
    id: UUID
    user_id: UUID
    role_id: Optional[UUID]
    name: str
    description: str
    key: Optional[bytearray]
    created: datetime
    last_used: Optional[datetime]
    enabled: bool
    visible: bool
    metadata: Optional[dict]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class User(BaseModel):
    id: UUID
    username: str
    role_id: UUID
    last_login: Optional[datetime]
    password: Optional[bytes]
    enabled: bool
    visible: bool
    created: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserRole(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True


class AvailableUserRoles(str, Enum):
    admin = "admin"
    user = "user"
    readonly = "read-only"
    transport = "transport"
    nobody = "nobody"


class HasuraRequest(BaseModel):
    """
    An object representing the JSON that Hasura sends to a webhook.

    Args:
        data (Dict[str, Any]): The JSON string that Hasura sent for this operation

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
    id: UUID
    trigger_name: str = None
    table_name: str = None
    table_schema: str = None
    created_at: datetime
    operation: str = None
    session_variables: Dict[str, str] = None
    old_data: Dict[str, str] = None
    new_data: Dict[str, str] = None

    def __init__(self, **data: Dict[str, Any]):
        """
        :param data: Dictionary representing that JSON string that Hasura sent for this operation
        """
        super().__init__(**data)
        self.id = UUID(str(data['id']))
        self.trigger_name = data['trigger']['name']
        self.table_name = data['table']['name']
        self.table_schema = data['table']['schema']
        self.created_at = dateutil.parser.parse(str(data['created_at']))
        self.operation = data['event']['op']
        self.session_variables = data['event']['session_variables']
        self.old_data = data['event']['data']['old']
        self.new_data = data['event']['data']['new']
