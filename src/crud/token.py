from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from pydantic import UUID4
from uuid import uuid4
import bcrypt

from src import models, schemas
from src.error import CustomDBError
from src.schemas import OAuthProvider
from src.crud import user


def validate_user(db: Session, auth_info: schemas.UserLoginRequest) -> models.UserToken:
    try:
        match_user = user.get_user_by_user_id(db, auth_info.user_id)

        if not match_user:
            raise CustomDBError(err_type=IntegrityError,
                                detail="아이디가 올바르지 않습니다.", tag='id')

        if not bcrypt.checkpw(auth_info.password, match_user.hashed_password):
            raise CustomDBError(err_type=IntegrityError,
                                detail="비밀번호가 올바르지 않습니다.", tag='password')

        # if prev token exist, remove it
        if match_user.token:
            db.delete(match_user.token)

        user_token_info = models.UserToken(user_id=match_user.id)

        db.add(user_token_info)
        db.commit()
        db.refresh(user_token_info)

        return user_token_info

    except Exception as e:
        raise CustomDBError(err_type=IntegrityError, detail=e.orig)


def check_token_available(db_token: models.UserToken, request_token: UUID4):
    if not db_token \
            or db_token.token_expire_date < datetime.now() \
            or db_token.token != request_token:

        return False

    return True


def check_refresh_token_available(db_token: models.UserToken, refresh_token: UUID4):
    if not db_token \
            or db_token.refresh_token_expire_date < datetime.now() \
            or db_token.refresh_token != refresh_token:

        return False

    return True


def get_token_by_user_id(db: Session, user_id: UUID4) -> models.UserToken:
    return db.query(models.UserToken).filter(
        models.UserToken.user_id == user_id).first()


def validate_token(db: Session, token: schemas.AccessRequest) -> bool:
    user_token = get_token_by_user_id(db, token.user_id)

    return check_token_available(user_token, token.token)


def refresh_token(db: Session, token: schemas.RefreshTokenRequest) -> Optional[models.UserToken]:
    user_token = get_token_by_user_id(db, token.user_id)

    if check_refresh_token_available(user_token, token.refresh_token):
        print("Check=----")
        user_token.token = uuid4()
        user_token.token_expire_date = min(
            user_token.refresh_token_expire_date, datetime.now() + timedelta(minutes=30))

        db.commit()

        return user_token
    raise CustomDBError(tag='expired')
