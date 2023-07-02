from fastapi import FastAPI, Response, Request, Header, status
from src.cors import origins, CORSMiddleware
from pydantic import BaseSettings
import requests
from urllib.parse import parse_qs
from src.routers import posts, users

from src import models
from src.database import engine

models.Base.metadata.create_all(bind=engine)


session = requests.Session()
session.headers.update({"accept": "application/json"})

app = FastAPI()

app.include_router(users.router)

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)


@app.get("/",
         status_code=200
         )
async def root():
    return {"hello": "world"}


@app.get("/login", status_code=200)
async def login(req: Request, response: Response):
    return {"bla": "bla"}


@app.post("/login/oauth/access_token", status_code=200)
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


@app.get("/login/oauth/user", status_code=200)
async def access_token(response: Response, Authorization: str = Header()):
    url = 'https://api.github.com/user'

    res = requests.get(
        url=url, headers={"Authorization": Authorization})

    if res.status_code != status.HTTP_200_OK:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return {"user_info": res.json()}
