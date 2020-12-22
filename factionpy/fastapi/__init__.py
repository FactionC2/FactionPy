from typing import Optional
import httpx

from factionpy.logger import log
from factionpy.config import AUTH_ENDPOINT, VERIFY_SSL
from factionpy.auth import User, standard_read, standard_write, standard_admin, validate_api_key

try:
    from fastapi import HTTPException, Depends
    from fastapi.security import OAuth2PasswordBearer
    from starlette.status import HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR
except Exception as exception:
    log("Could not load FastAPI python module. Install it before using this functionality.")
    raise exception


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{AUTH_ENDPOINT}/login/")
client = httpx.AsyncClient(verify=VERIFY_SSL)


async def user_is_authenticated(api_key: str = Depends(oauth2_scheme)) -> Optional[User]:
    """
    :param api_key: The value of the Authorization heard to be verified
    :return: User or None
    """
    log(f"got api key {api_key}", "debug")
    try:
        return await validate_api_key(api_key)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


async def user_has_read_access(user: User = Depends(user_is_authenticated)) -> User:
    if user.role in standard_read:
        return user
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=f"{user.username} is not authorized to perform this action"
        )


async def user_has_write_access(user: User = Depends(user_is_authenticated)) -> User:
    if user.role in standard_write:
        return user
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=f"{user.username} is not authorized to perform this action"
        )


async def user_has_admin_access(user: User = Depends(user_is_authenticated)) -> User:
    if user.role in standard_admin:
        return user
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=f"{user.username} is not authorized to perform this action"
        )
