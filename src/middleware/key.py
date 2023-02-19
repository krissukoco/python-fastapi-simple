from fastapi import Security
from fastapi.security import APIKeyHeader

from ..config import Config
from ..response.errors import APIKeyException

_api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def confirm_api_key(api_key: str = Security(_api_key_header)):
    if api_key == Config.API_KEY:
        return api_key
    raise APIKeyException()