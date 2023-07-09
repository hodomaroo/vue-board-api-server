from fastapi import Response, Header, status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import requests

from src.database import get_db
from src.session import session
from src.crud import user, token
from src import schemas
from src.error import CustomDBError

router = APIRouter(prefix="/login", tags=['login'])


@router.post("/oauth/access_token", status_code=200)
async def access_token(client_id: str, client_secret: str, code: str, response: Response):
    url = 'https://github.com/login/oauth/access_token'
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code
    }

    res = session.post(
        url=url, data=payload)

    if res.status_code != status.HTTP_200_OK:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return {"token_info": res.json()}


@router.get("/oauth/user", status_code=200)
async def user_info(response: Response, Authorization: str = Header()):
    print(Authorization)
    url = 'https://api.github.com/user'
    res = requests.get(
        url=url, headers={"Authorization": Authorization})

    if res.status_code != status.HTTP_200_OK:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return {"user_info": res.json()}


@router.post("", status_code=status.HTTP_200_OK, response_model=Optional[schemas.TokenResponse])
def login(response: Response, login_request: schemas.UserLoginRequest, db: Session = Depends(get_db)):
    try:
        return token.validate_user(db, login_request)
    except CustomDBError as e:
        raise HTTPException(
            headers={'tag': e.tag}, status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)
