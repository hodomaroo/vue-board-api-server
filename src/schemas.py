from typing import List, Union, Text
from pydantic import BaseModel, UUID4
from datetime import datetime
from enum import Enum


class UserType(Enum):
    OAUTH = 'OAtuth'
    LOCAL = 'Local'


class OAuthProvider(Enum):
    GOOGLE = 'Google'
    LOCAL = 'Local'


class PostBase(BaseModel):
    title: str
    contents: Text


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: UUID4
    author_id: UUID4
    created_date: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str | None
    user_type: UserType


class UserCreate(UserBase):
    password: str | None


class User(UserBase):
    id: UUID4
    created_date: datetime
    posts: List[Post] = []

    class Config:
        orm_mode = True


class OAuthUser(BaseModel):
    id: str
    user_id: UUID4
    oauth_provider: OAuthProvider
    user: User

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str
    expireDate: datetime
    user: User

    class Config:
        orm_mode = True
