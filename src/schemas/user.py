from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    index : int
    firstname : str
    surname : str
    patronimic : Optional [str] = None
    email : str
    password : str