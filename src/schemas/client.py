from typing import Optional
from pydantic import BaseModel
from typing import Optional


class Client(BaseModel):
    counter: Optional[int] = 0


class ClientEdit(BaseModel):
    counter: Optional[int] = 0
    
