from pydantic import BaseModel
from typing import Optional


class Client(BaseModel):
    index : int
    rating : Optional [float] = 0
    counter : Optional [int] = 0
