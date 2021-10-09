from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", status_code=200)
async def get_user():
    pass


@router.post("/", status_code=200)
async def create_user():
    pass


@router.patch("/", status_code=200)
async def update_user():
    pass


@router.delete("/", status_code=200)
async def delete_user():
    pass
