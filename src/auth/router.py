from fastapi import APIRouter, HTTPException, Depends

from .schema import Login, Register, UserBase, LoginResponse, EmailOrPasswordIncorrectException, EmailAlreadyExistsException
from ..model.user import User
from ..middleware.token import get_user_email_from_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/register", response_model=UserBase)
def register(body: Register):
    # Check if password is the same as confirm_password
    if body.password != body.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Password and confirm password must be the same",
        )
    u = User.create(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        raw_password=body.password,
    )
    if u is None:
        raise EmailAlreadyExistsException()
    return UserBase(email=u.email, first_name=u.first_name, last_name=u.last_name, created_at=u.created_at)

@router.post("/login", response_model=LoginResponse)
def login(body: Login):
    u = User.find(body.email)
    if u is None:
        raise EmailOrPasswordIncorrectException()
    # Verify password
    if not u.verify_password(body.password):
        raise EmailOrPasswordIncorrectException()
    user = UserBase(email=u.email, first_name=u.first_name, last_name=u.last_name, created_at=u.created_at)
    return LoginResponse(token=u.issue_jwt(), user=user)

@router.get("/refresh", response_model=UserBase)
def refresh(email_dep: str = Depends(get_user_email_from_token)):
    u = User.find(email_dep)
    if u is None:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid",
        )
    user = UserBase(email=u.email, first_name=u.first_name, last_name=u.last_name, created_at=u.created_at)
    return user

