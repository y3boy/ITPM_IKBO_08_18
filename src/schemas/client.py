from typing import Optional
from pydantic import BaseModel
from typing import Optional


class Client(BaseModel):
    index : int
    counter :  Optional [int] = 0
    
