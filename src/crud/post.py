from .. import models, schemas
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4
from src.error import CustomDBError

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
