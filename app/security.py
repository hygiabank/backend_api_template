from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Annotated
from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi import Depends
from fastapi.security import APIKeyCookie

from app.exceptions import Unauthorized
from app.settings import settings

SECRET_KEY = settings.JWT_AUTH_SECRET
ALGORITHM = settings.JWT_ALGORITHM
JWT_EXPIRE = settings.JWT_EXPIRES
JWT_KEY_NAME = settings.JWT_KEY_NAME

jwt_cookie_scheme = APIKeyCookie(name=JWT_KEY_NAME, auto_error=True)

class TokenData(BaseModel):
    sub: str
    
def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=JWT_EXPIRE)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)

    except JWTError as e:
        raise Unauthorized(f"Could not validate credentials: {e}")
    
    return token_data

def set_token_cookie(user_data: TokenData, response: Response) -> str:
    user_data_dict = user_data.model_dump(exclude_defaults=True, exclude_unset=True, exclude_none=True)
    token = create_token(user_data_dict, timedelta(seconds=JWT_EXPIRE))
    response.set_cookie(key=JWT_KEY_NAME, value=token, httponly=True, max_age=JWT_EXPIRE)
    return token

def revoke_token_cookie(response: Response) -> None:
    response.delete_cookie(key=JWT_KEY_NAME)


def get_current_user(token: Annotated[str, Depends(jwt_cookie_scheme)]) -> str:
    print(token)
    token_data = decode_token(token)

    user_id: str = token_data.sub

    if user_id is None:
        raise Unauthorized("Could not validate credentials")

    return user_id

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return password_context.hash(password)

def authenticate_user(provided_password: str, user_password) -> None:
    if not verify_password(provided_password, user_password):
        raise Unauthorized("Invalid password")
    

def init_security(app: FastAPI):
    app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    if not settings.DEBUG:
        app.add_middleware(HTTPSRedirectMiddleware)
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=[settings.JWT_TOKEN_AUDIENCE])
        