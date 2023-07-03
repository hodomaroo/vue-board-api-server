from fastapi import APIRouter, Header, Response, status, Depends, HTTPException
from src.database import get_db
from sqlalchemy.orm import Session
from src import schemas, models
from src.crud import user as crud
from src.error import CustomDBError
from typing import Optional
router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db)):
    # print("CHECK")
    return crud.get_users(db)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_user_by_user_id(response: Response, user_id: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_user_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not Exist")
    return user


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(response: Response, user: schemas.UserCreate, oauth: Optional[schemas.OAuthBase] = None, db: Session = Depends(get_db)):
    try:
        if user.user_type == schemas.UserType.LOCAL:
            db_user = crud.create_user(db=db, user=user)
        else:
            db_user = crud.create_oauth_user(
                db=db, user=user, oauth=oauth)

            print(schemas.User.from_orm(db_user))

        return db_user

    except CustomDBError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail
        )
    except Exception as e:
        print(str(e))
