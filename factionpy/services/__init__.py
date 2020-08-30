import requests
from factionpy.config import AUTH_ENDPOINT
from factionpy.logger import log


def validate_authorization_header(header_value: str, verify_ssl: bool = True):
    log(f"got header {header_value}", "debug")
    success = "false"
    result = None
    try:
        headers = {"Authorization": header_value}
        url = f"{AUTH_ENDPOINT}/verify/"
        log(f"using url: {url}", "debug")
        r = requests.get(url, headers=headers, verify=verify_ssl).json()
        log(f"got response {r}", "debug")
        if r['success'] == "true":
            success = "true"
            result = r
    except Exception as e:
        result = e
    rsp = {"success": success, "result": result}
    log(f"returning: {rsp}", "debug")
    return rsp
