from pydantic import BaseModel
from src.models.token import Token
from src.models.user import UserOut
from src.models.walker import WalkerOut
from src.models.order import OrderOut
from src.models.dog import DogOut
from typing import Optional


class UserToken(BaseModel):
    User: Optional[UserOut]
    Token: Optional[Token]


class UserWalker(BaseModel):
    User: Optional[UserOut]
    Walker: Optional[WalkerOut]


class OrderUserDog(BaseModel):
    Order: Optional[OrderOut]
    User: Optional[UserOut]
    Dog: Optional[DogOut]

