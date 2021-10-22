from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from src.database.models import User


router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", status_code=200)
async def auth_user(user_info: User, ):
    pass
    # Взять данные с запроса из базы и сверить с паролем в базе данных
    # При положительном ответе вернуть True else False


@router.post("/", status_code=200)
async def create_user(user_info: User):
    pass  # func from crud.py


@router.patch("/", status_code=200)
async def update_user(user_info: User):
    pass  # func from crud.py


@router.delete("/", status_code=200)
async def delete_user(user_info: User):
    pass  # func from crud.py
