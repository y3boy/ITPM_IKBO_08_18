from pydantic import BaseModel
from typing import Optional


class Dog(BaseModel):
    breed: str
    nickname: str
    avatar_url: str
