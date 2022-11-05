from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int


class UserInDB(User):
    hashed_password: str


class TagBase(BaseModel):
    title: str

    class Config:
        orm_mode = True


class TagUpdate(TagBase):
    pass


class Tag(TagBase):
    id: int
    user_id: int