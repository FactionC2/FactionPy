import requests
from factionpy.config import AUTH_ENDPOINT


def validate_api_key(header_value):
    headers = {'Authorization': f"{header_value}"}
    resp = requests.get(f"{AUTH_ENDPOINT}/verify/", headers=headers)
    return resp.json()


