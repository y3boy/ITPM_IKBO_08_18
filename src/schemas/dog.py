from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Dog(BaseModel):
    breed: str
    nickname: str
    avatar_url: str
    size_in_kg: int
    date_of_birth: datetime


class DogEdit(BaseModel):
    breed: Optional[str]
    nickname: Optional[str]
    avatar_url: Optional[str]
    size_in_kg: Optional[int]
    date_of_birth: Optional[datetime]
