from pydantic import BaseModel
from typing import Union


class UserAuthDetails(BaseModel):
    id = int
    username: str
    email: str
    fullname: Union[str, None] = None
    password: str


class UserCreate(UserAuthDetails):
    pass


class UserInDB(UserAuthDetails):
    hashed_password: str


class UserOut(BaseModel):
    username: str
    email: str
    fullname: Union[str, None] = None


class SystemUser(UserOut):
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
