import requests
from factionpy.config import AUTH_ENDPOINT


def validate_authorization_header(header_value):
    success = False
    result = None
    try:
        headers = {"Authorization": header_value}
        r = requests.get(f"{AUTH_ENDPOINT}/verify/", headers=headers).json()
        if r['success'] == "True":
            success = True
            result = r
    except Exception as e:
        result = e
    return {"success": success, "result": result}
