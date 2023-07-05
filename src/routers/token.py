from fastapi import Response, Header, status, APIRouter
from src.session import session
import requests


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
