from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    tag_id: int


class UserInDB(User):
    hashed_password: str


class TagBase(BaseModel):
    title: str


class Tag(TagBase):
    id: int