from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class OrderBase(BaseModel):
    walker_id: int
    client_dog_id: int
    datetime_of_creation: datetime
    datetime_of_walking: datetime
    numbers_of_hours: int
    description: Optional[str]


class OrderEdit(BaseModel):
    walker_took_order: Optional[bool]
    client_confirmed_execution: Optional[bool]
    paid: Optional[bool]


class Order(BaseModel):
    client_id: int
    walker_id: int
    client_dog_id: int
    datetime_of_creation: datetime
    datetime_of_walking: datetime
    numbers_of_hours: int
    price: int
    commission: int
    description: Optional[str]

    walker_took_order: Optional[bool]
    client_confirmed_execution: Optional[bool]
    paid: Optional[bool]