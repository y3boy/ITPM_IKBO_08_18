from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.schemas.user import User

from src.database import crud
from src.app.dependencies import get_db

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", status_code=200)
async def auth_user(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    user = crud.user_read_by_username(username=form_data.username, session=session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    if not crud.validate_password(password=form_data.password, hashed_password=user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    return crud.create_user_token(user_id=user["id"], session=session)


@router.post("/", status_code=200)
async def create_user(user_info: User, session: Session = Depends(get_db)):
    return crud.client_create(user_info, session)


@router.patch("/", status_code=200)
async def update_user(user_info: User, session: Session = Depends(get_db)):
    return crud.walker_create(user_info, session)


@router.delete("/", status_code=200)
async def delete_user(user_info: User, session: Session = Depends(get_db)):
    return crud.user_delete(user_info, session)
