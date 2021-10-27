from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from src.schemas.user import User

from src.database import crud
from src.app.dependencies import get_db

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", status_code=200)
async def auth_user(user_info: str, session: Session = Depends(get_db)):
    return crud.user_authorization(user_info, session)


@router.post("/", status_code=200)
async def create_user(user_info: User, session: Session = Depends(get_db)):
    return crud.client_create(user_info, session)


@router.patch("/", status_code=200)
async def update_user(user_info: User, session: Session = Depends(get_db)):
    return crud.walker_create(user_info, session)


@router.delete("/", status_code=200)
async def delete_user(user_info: User, session: Session = Depends(get_db)):
    return crud.user_delete(user_info, session)
