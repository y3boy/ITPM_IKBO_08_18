from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    hashed_password: str
    fullname: str
    phone: str
    email: str
