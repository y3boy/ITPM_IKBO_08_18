from typing import Optional, List
from pydantic import BaseModel, root_validator


class WalkerOut(BaseModel):
    id: int
    rating: Optional[float]
    counter: int
    price_per_hour: int
    stations: List[str]
    min_dog_size_in_kg: Optional[int]
    max_dog_size_in_kg: Optional[int]
    min_dog_age_in_years: Optional[int]
    max_dog_age_in_years: Optional[int]
    schedule: Optional[str]
    about_walker: Optional[str]

    class Config:
        orm_mode = True


class WalkerCreate(BaseModel):
    price_per_hour: int
    stations: List[str]
    min_dog_size_in_kg: Optional[int]
    max_dog_size_in_kg: Optional[int]
    min_dog_age_in_years: Optional[int]
    max_dog_age_in_years: Optional[int]
    schedule: Optional[str]
    about_walker: Optional[str]


class WalkerUpdate(BaseModel):
    price_per_hour: int
    counter: int
    stations: List[str]
    min_dog_size_in_kg: Optional[int]
    max_dog_size_in_kg: Optional[int]
    min_dog_age_in_years: Optional[int]
    max_dog_age_in_years: Optional[int]
    schedule: Optional[str]
    about_walker: Optional[str]