from typing import Optional
from distutils.util import strtobool
import httpx

from factionpy.logger import log
from factionpy.config import AUTH_ENDPOINT
from factionpy.models import User

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

