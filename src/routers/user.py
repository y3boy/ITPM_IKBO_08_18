from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.schemas.user import UserBase

from src.database import crud
from src.app.dependencies import get_db

from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.user import TokenBase

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/auth", status_code=200, response_model=TokenBase)
async def auth_user(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    user = crud.user_read_by_username(username=form_data.username, session=session)
    print(user)
    if not user:
        print('test1')
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    if not crud.validate_password(password=form_data.password, hashed_password=user.hashed_password):
        print('test2')
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    print('test3')
    result = crud.create_user_token(user_id=user.id, session=session)
    print('---------')
    print(result)
    return result


@router.post("/client", status_code=200)
async def create_client(user_info: UserBase, session: Session = Depends(get_db)):
    return crud.client_create(user_info, session)


@router.post("/walker", status_code=200)
async def create_walker(user_info: UserBase, session: Session = Depends(get_db)):
    return crud.walker_create(user_info, session)


@router.patch("/", status_code=200)
async def update_user(user_id: int, user_info: UserBase, session: Session = Depends(get_db)):
    return crud.user_update(user_id, user_info, session)


@router.delete("/", status_code=200)
async def delete_user(user_id: int, session: Session = Depends(get_db)):
    return crud.user_delete(user_id, session)
