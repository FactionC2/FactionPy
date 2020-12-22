from uuid import UUID
from datetime import datetime
from typing import Optional
from distutils.util import strtobool

from pydantic import BaseModel
import httpx

from factionpy.logger import log
from factionpy.config import AUTH_ENDPOINT

VERIFY_SSL = False

client = httpx.AsyncClient(verify=VERIFY_SSL)

standard_read = [
    'admin',
    'super-user',
    'service',
    'user',
    'read-only'
]

standard_write = [
    'admin',
    'super-user',
    'service',
    'user'
]

standard_admin = [
    'admin',
    'super-user'
]


class User(BaseModel):
    id: UUID
    username: str
    role: str
    last_login: datetime
    enabled: bool
    visible: bool
    created: datetime
    api_key: str
    api_key_description: str


async def validate_api_key(api_key: str) -> Optional[User]:
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        url = f"{AUTH_ENDPOINT}/verify/"
        log(f"using url: {url}", "debug")
        response = await client.get(url, headers=headers)
        r_json = response.json()
        log(f"got response {r_json}", "debug")
        if bool(strtobool(r_json['success'])):
            log(f"returning user: {r_json['data']}", "debug")
            user = User.parse_obj(r_json["data"])
            return user
    except Exception as e:
        log(f"Error validating API key: {e}")
    return None

