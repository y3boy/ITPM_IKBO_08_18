from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    index: int
    username: str
    password: str
    fullname: str
    phone: str
    email: str
