from pydantic import BaseModel, EmailStr
from ..response.errors import BaseHTTPException
from ..response.code import ErrorCode

class Login(BaseModel):
    email: EmailStr
    password: str

class Register(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    created_at: int

class LoginResponse(BaseModel):
    token: str
    user: UserBase

# ========================== HTTP EXCEPTIONS ==========================
class EmailOrPasswordIncorrectException(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            code=ErrorCode.EMAIL_OR_PASSWORD_INCORRECT,
            message="Email or password is incorrect",
        )

class EmailAlreadyExistsException(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            code=ErrorCode.EMAIL_ALREADY_EXIST,
            message="Email already exists",
        )