import jwt
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..config import Config
from ..response.errors import BearerTokenMissingException, BearerTokenExpiredException, BearerTokenInvalidException, BearerTokenMalformedException

_auth_header = HTTPBearer()

def get_user_email_from_token(auth: str = Security(_auth_header)):
    if auth is None:
        raise BearerTokenMissingException()
    split = auth.credentials.split(" ")
    if len(split) != 2:
        raise BearerTokenMalformedException()
    if split[0] != "Bearer":
        raise BearerTokenMalformedException()
    token = split[1]
    print("TOKEN: ", token)
    try:
        payload = jwt.decode(
            token, 
            Config.JWT_SECRET, 
            algorithms=['HS256'],
            audience='github.com/krissukoco/python-fastapi-simple',
        )
    except jwt.ExpiredSignatureError:
        raise BearerTokenExpiredException()
    except Exception as e:
        raise BearerTokenInvalidException()
    if 'sub' not in payload:
        raise BearerTokenInvalidException()
    return payload['sub']