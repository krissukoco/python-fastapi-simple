from enum import Enum

class ErrorCode(int, Enum):
    OK = 0
    # Auth errors
    UNAUTHORIZED = 10000
    API_KEY_INVALID = 10001
    BEARER_TOKEN_MISSING = 10010
    BEARER_TOKEN_MALFORMED = 10011
    BEARER_TOKEN_INVALID = 10012
    BEARER_TOKEN_EXPIRED = 10013
    EMAIL_OR_PASSWORD_INCORRECT = 10020
    EMAIL_ALREADY_EXIST = 10021
    # Validation errors
    VALIDATION_ERROR = 20000
    # Resource errors: 30000 - 39999
    POST_NOT_FOUND = 20001
    