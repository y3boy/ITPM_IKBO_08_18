from pydantic import BaseModel


class Client(BaseModel):
    index : int
    description : str
