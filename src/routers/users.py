from fastapi import APIRouter, Header, Response, status, Depends, HTTPException
from src.database import get_db
from sqlalchemy.orm import Session
from src import schemas, models
from src.crud import user as crud

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.get("/{user_id}", tags=['users'], status_code=200, response_model=schemas.User)
async def get_user_by_user_id(response: Response, user_id: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_user_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not Exist")
    return user
