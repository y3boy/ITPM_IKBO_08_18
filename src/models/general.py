from pydantic import BaseModel
from src.models.token import Token
from src.models.user import UserOut
from src.models.walker import WalkerOut
from typing import Optional


class UserToken(BaseModel):
    user: Optional[UserOut]
    token: Optional[Token]


class UserWalker(BaseModel):
    user: Optional[UserOut]
    walker: Optional[WalkerOut]
