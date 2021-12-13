from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DogOut(BaseModel):
    id: int
    breed: str
    nickname: str
    size_in_kg: Optional[int]
    date_of_birth: Optional[datetime]

    user_id: int

    class Config:
        orm_mode = True


class DogCreate(BaseModel):
    breed: str
    nickname: str
    size_in_kg: Optional[int]
    date_of_birth: Optional[datetime]


class DogUpdate(BaseModel):
    breed: str
    nickname: str
    size_in_kg: Optional[int]
    date_of_birth: Optional[datetime]