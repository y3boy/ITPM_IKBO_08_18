from pydantic import BaseModel
from typing import FrozenSet


class Client(BaseModel):
    index : int
    description : str
