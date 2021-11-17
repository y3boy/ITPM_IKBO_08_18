from pydantic import BaseModel
from typing import Optional


class Walker(BaseModel):
    rating: Optional[float] = 0
    counter: Optional[int] = 0

    region_code: int
    price_per_hour: int
    practice_in_year: int
    min_dog_size_in_kg: Optional[int]
    max_dog_size_in_kg: Optional[int]
    min_dog_age_in_years: Optional[int]
    max_dog_age_in_years: Optional[int]

    schedule: Optional[str]
    about_walker: Optional[str]


class WalkerEdit(BaseModel):
    rating: Optional[float] = 0
    counter: Optional[int] = 0

    region_code: Optional[int]
    price_per_hour: Optional[int]
    practice_in_year: Optional[int]
    min_dog_size_in_kg: Optional[int]
    max_dog_size_in_kg: Optional[int]
    min_dog_age_in_years: Optional[int]
    max_dog_age_in_years: Optional[int]

    schedule: Optional[str]
    about_walker: Optional[str]


class WalkerCreate(BaseModel):
    region_code: int
    price_per_hour: int
    practice_in_year: int
    min_dog_size_in_kg: Optional[int]
    max_dog_size_in_kg: Optional[int]
    min_dog_age_in_years: Optional[int]
    max_dog_age_in_years: Optional[int]

    schedule: Optional[str]
    about_walker: Optional[str]