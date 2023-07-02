from . import models, schemas
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4
from src.error import CustomDBError
# 암호화 모듈 import
import bcrypt


# User CRUD API
def get_user(db: Session, user_id: UUID4) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_user_id(db: Session, user_id: UUID4) -> models.User | None:
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users_by_name(db: Session, name: str) -> List[models.User]:
    return db.query(models.User).filter(models.User.name == name).all()


def create_user(db: Session, user: schemas.UserCreate):
    try:
        password: str = user.password.encode('utf-8')
        hashed_password: str = bcrypt.hashpw(password, bcrypt.gensalt())
        db_user = models.User(email=user.email, name=user.name,
                              user_type=user.user_type, hashed_password=hashed_password)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    except IntegrityError as e:
        raise CustomDBError(err_type=IntegrityError, detail=e.orig)

    return db_user

# get api for oauth user


def get_oauth_user_by_id(db: Session, id: str) -> models.OAuthUser | None:
    return db.query(models.OAuthUser).filter(models.OAuthUser.id == id).first()


def create_oauth_user(db: Session, oauth_user: schemas.OAuthUser, user_id: UUID4) -> models.User:
    try:
        db_oauth_user = models.OAuthUser(
            id=oauth_user.id,
            user_id=user_id,

            oauth_provider=oauth_user.oauth_provider
        )
        db.add(db_oauth_user)
        db.commit()
        db.refresh(db_oauth_user)

    except IntegrityError as e:
        raise CustomDBError(err_type=IntegrityError, detail=e.orig)

    return db_oauth_user

    # Post CRUD API


def get_post(db: Session, post_id: UUID4) -> models.Post | None:
    return db.query(models.Post).filter(models.Post.id == post_id).first()

# Get Specific Number of Post for Paging


def get_post(db: Session, offset: int, count: int) -> List[models.Post]:
    return db.query(models.Post).offset(offset).limit(count)


def create_post(db: Session, post: schemas.PostCreate, author_id: UUID4) -> models.Post:

    try:
        db_post = models.Post(
            title=post.title, contents=post.contents, author_id=author_id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)

    except IntegrityError as e:
        raise CustomDBError(err_type=IntegrityError, detail=e.orig)
    return db_post
