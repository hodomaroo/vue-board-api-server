from fastapi import FastAPI
from fastapi import FastAPI
from src.cors import origins, CORSMiddleware
from pydantic import BaseSettings
import requests

from src import models
from src.database import engine
from src.routers import posts, token, users

import uvicorn
from src.cors import origins, CORSMiddleware
from pydantic import BaseSettings
import requests

from src import models
from src.database import engine
from src.routers import posts, token, users

import uvicorn
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(token.router)

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)


@app.get("/")
def func():
    return {'hello': "world!"}


if __name__ == '__main__':
    uvicorn.run('entrypoint:app',
                host='127.0.0.1', port=8000, reload=True)
