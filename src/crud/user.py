from .. import models, schemas
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4
from src.error import CustomDBError
from src.schemas import OAuthProvider
# 암호화 모듈 import
import bcrypt


# User CRUD API
def get_user(db: Session, user_id: UUID4) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_user_id(db: Session, user_id: UUID4) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users_by_name(db: Session, name: str) -> List[models.User]:
    return db.query(models.User).filter(models.User.name == name).all()


def create_user(db: Session, user: schemas.UserCreate, commit: bool = True) -> Optional[models.User]:
    try:
        if user.user_type == schemas.UserType.LOCAL:
            password: str = user.password.encode('utf-8')
            hashed_password: str = bcrypt.hashpw(password, bcrypt.gensalt())
            db_user = models.User(user_id=user.user_id, email=user.email, name=user.name,
                                  user_type=user.user_type, hashed_password=hashed_password)
        else:
            db_user = models.User(user_id=user.user_id, email=user.email, name=user.name,
                                  user_type=user.user_type)

        db.add(db_user)

        print(f"db_user_id : {db_user.id}")
        if commit:
            db.commit()
            db.refresh(db_user)
        else:
            db.flush()

    except IntegrityError as e:
        raise CustomDBError(err_type=IntegrityError, detail=str(e))

    return db_user


def get_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()

# get api for oauth user


def get_oauth_user_by_id(db: Session, id: str) -> Optional[models.OAuthUser]:
    return db.query(models.OAuthUser).filter(models.OAuthUser.id == id).first()


def create_oauth_user(db: Session, user: schemas.User, oauth: schemas.OAuthBase) -> Optional[models.User]:
    try:

        db_user = create_user(db, user, commit=False)

        oauth_user = models.OAuthUser(
            user_id=db_user.id,
            oauth_provider=oauth.oauth_provider)

        db.add(oauth_user)

        db.commit()

        db.refresh(db_user)
        db.refresh(oauth_user)

        res = db.query(models.User).filter(
            models.User.id == db_user.id).first()

        return res

    except IntegrityError as e:
        raise CustomDBError(err_type=IntegrityError, detail=e.orig)

    # Post CRUD API


def authenticate_user(db: Session, auth_info: schemas.UserLogin) -> models.User:
    try:
        match_user = get_user_by_user_id(db, auth_info.user_id)

        if not match_user:
            raise CustomDBError(err_type=IntegrityError,
                                detail="아이디가 올바르지 않습니다.", tag='id')

        if not bcrypt.checkpw(auth_info.password, match_user.hashed_password):
            raise CustomDBError(err_type=IntegrityError,
                                detail="비밀번호가 올바르지 않습니다.", tag='password')

        return match_user

    except Exception as e:
        raise CustomDBError(err_type=IntegrityError, detail=e.orig)
