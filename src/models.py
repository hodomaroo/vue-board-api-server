from sqlalchemy import DateTime, Column, Uuid, String, ForeignKey, Text, Enum, CheckConstraint
from sqlalchemy.orm import relationship

from .database import Base

import datetime
import uuid


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4())
    title = Column(String, nullable=False, index=True)

    contents = Column(Text)

    created_date = Column(DateTime, default=datetime.now())
    author_id = Column(Uuid, ForeignKey("users.id"))

    author = relationship("User", back_populates='posts')


class OAuthUser(Base):
    __tablename__ = 'oauth_users'

    id = Column(String, primary_key=True)
    user_id = Column(Uuid, ForeignKey('users.id'), nullable=False)

    oauth_provider = Column(Enum('GitHub', 'Google'), name='user_type_enum')
    user = relationship("User", back_populates='user')


class User(Base):
    __tablename__ = 'users'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    hashed_password = Column(String)
    email = Column(String, nullable=False, unique=True)
    user_type = Column(Enum('OAuth', 'Local'), name='user_type_enum')

    created_date = Column(DateTime, default=datetime.now())
    posts = relationship('Post', back_populates='author')
    user = relationship('OAuthUser', back_populates='user')

    __table_args__ = (
        CheckConstraint(
            "(user_type = 'OAuth' AND hashed_password IS NULL) OR (user_type != 'OAuth' AND password IS NOT NULL)",
            name='password_validation_by_user_type'
        )
    )
