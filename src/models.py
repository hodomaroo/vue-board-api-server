from sqlalchemy import DateTime, Column, Uuid, String, ForeignKey, Text, Enum, CheckConstraint, Integer
from sqlalchemy.orm import relationship

from .database import Base
from datetime import datetime, timedelta
import uuid
from src.schemas import UserType, OAuthProvider


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4())
    title = Column(String, nullable=False, index=True)

    contents = Column(Text)

    created_date = Column(DateTime, default=datetime.now())
    author_id = Column(Uuid, ForeignKey("users.id"))

    # 관계가 두개 이상인 경우, foreign_key = ~~로 명시 가능
    author = relationship("User", back_populates='posts',
                          foreign_keys=[author_id])


class OAuthUser(Base):
    __tablename__ = 'oauth_users'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4())
    user_id = Column(Uuid, ForeignKey('users.id'), nullable=False)

    oauth_provider = Column(Enum(OAuthProvider), name='oauth_provider')
    user = relationship("User", back_populates='oauth', foreign_keys=[user_id])


class User(Base):
    __tablename__ = 'users'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4())
    user_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String)
    email = Column(String, nullable=False, unique=True)
    user_type = Column(Enum(UserType), name='user_type')

    created_date = Column(DateTime, default=datetime.now())
    posts = relationship('Post', back_populates='author',
                         foreign_keys='Post.author_id')
    oauth = relationship('OAuthUser', back_populates='user',
                         foreign_keys='OAuthUser.user_id', uselist=False)
    token = relationship('UserToken', back_populates='user',
                         foreign_keys='UserToken.user_id', uselist=False)

    CheckConstraint(
        "(user_type = 'OAUTH' AND hashed_password IS NULL) OR (user_type == 'LOCAL' AND hashed_password IS NOT NULL)",
        name='password_validation_by_user_type'
    ),
    CheckConstraint(
        "(user_type = 'OAUTH') OR (user_id IS NOT NULL)",
        name='id_validation_by_user_type'
    ),


# using User Token when user logined to service


class UserToken(Base):
    __tablename__ = 'tokens'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4())
    user_id = Column(Uuid, ForeignKey('users.id'))
    token = Column(String)
    # Default token duration is 1hour
    expireDate = Column(DateTime)

    user = relationship('User', back_populates='token', foreign_keys=[user_id])
