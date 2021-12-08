from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class OrderOut(BaseModel):
    id: int
    datetime_of_creation: datetime
    datetime_of_walking: datetime
    numbers_of_hours: int
    price_without_commission: int
    commission: int
    description: Optional[str]

    rating: Optional[float]
    review: Optional[str]

    walker_took_order: Optional[bool]
    client_confirmed_execution: Optional[bool]
    paid: Optional[bool]

    client_id: int
    walker_id: int
    dog_id: int

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    datetime_of_walking: datetime
    numbers_of_hours: int
    description: Optional[str]


class OrderUpdate(BaseModel):
    rating: Optional[float]
    review: Optional[str]

    walker_took_order: Optional[bool]
    client_confirmed_execution: Optional[bool]
    paid: Optional[bool]
