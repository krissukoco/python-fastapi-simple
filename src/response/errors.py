from fastapi import HTTPException

from src.response.code import ErrorCode

# Base class for all HTTP exceptions
class BaseHTTPException(Exception):
    def __init__(self, status_code: int, code: ErrorCode, message: str = None, headers: dict = None):
        self.status_code = status_code
        self.code = code
        self.message = message if message is not None else ""
        self.headers = headers if headers is not None else {}

# ========================= API KEY =========================
class APIKeyException(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            code=ErrorCode.API_KEY_INVALID,
            message="Invalid API key",
        )

# ========================= BEARER TOKEN =========================
class BearerTokenMissingException(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            code=ErrorCode.BEARER_TOKEN_MISSING,
            message="Token missing",
        )
    
class BearerTokenMalformedException(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            code=ErrorCode.BEARER_TOKEN_MALFORMED,
            message="Token malformed",
        )

class BearerTokenInvalidException(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            code=ErrorCode.BEARER_TOKEN_INVALID,
            message="Token invalid",
        )

class BearerTokenExpiredException(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            code=ErrorCode.BEARER_TOKEN_EXPIRED,
            message="Token expired",
        )