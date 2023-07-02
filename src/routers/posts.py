from fastapi import APIRouter, Header, Response, status, Depends, HTTPException
from src.database import get_db
from sqlalchemy.orm import Session
from src import schemas, models
from src.crud import post

router = APIRouter(
    prefix="/items",
    tags=['items']
)


@router.get("/{post_id}", status_code=200, response_model=schemas.User)
async def get_post_by_post_id(response: Response, post_id: str, db: Session = Depends(get_db)):
    post = post.get_user_by_user_id(db=db, user_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not Exist")
    return post

