from __future__ import annotations
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, UUID4, Field
from typing import List, Union, Text, Optional


class UserType(Enum):
    OAUTH = 'OAUTH'
    LOCAL = 'LOCAL'


class OAuthProvider(Enum):
    GOOGLE = 'GOOGLE'


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
    user_id: str
    name: str | None
    email: str | None
    user_type: UserType


class UserCreate(UserBase):
    password: str | None


class User(UserBase):
    id: UUID4
    created_date: datetime
    posts: List[Post] | None
    oauth: Optional[OAuthUser] = Field(default=None)

    class Config:
        orm_mode = True


class OAuthBase(BaseModel):
    oauth_provider: OAuthProvider


class OAuthUser(OAuthBase):
    id: UUID4
    user_id: UUID4

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    token: UUID4
    refresh_token: UUID4

    token_expire_date: datetime
    refresh_token_expire_date: datetime

    class Config:
        orm_mode = True


##### Validate Token #####

class AccessRequest(BaseModel):
    user_id: UUID4
    token: UUID4


class AccessResponse(BaseModel):
    isValid: bool


##### Refresh Token #####
class RefreshTokenRequest(BaseModel):
    user_id: str
    refresh_token: UUID4


class RefreshTokenResponse(BaseModel):
    isValid: bool
    # Just Refrence TokenResponse Model. It doesn't need to Config orm_mode
    token: Optional[UUID4]

    class config:
        orm_mode = True


##### Login #####

class UserLoginRequest(BaseModel):
    user_id: UUID4
    password: str


User.update_forward_refs()
