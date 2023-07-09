from fastapi import Response, Header, status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from src.database import get_db
from src.crud import user, token
from src import schemas
from src.error import CustomDBError


router = APIRouter(
    prefix="/token",
    tags=['token']
)


# check token is validate
@router.post("", status_code=status.HTTP_200_OK, response_model=Optional[schemas.AccessResponse])
def validate_token(response: Response, tokenRequest: schemas.AccessRequest, db: Session = Depends(get_db)):
    return token.validate_token(db, tokenRequest)


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=schemas.RefreshTokenResponse)
def refresh_token(tokenRefreshInfo: schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        return token.refresh_token(db, tokenRefreshInfo)
    except CustomDBError as e:
        raise HTTPException(detail=e.tag)
