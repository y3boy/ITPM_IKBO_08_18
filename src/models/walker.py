from typing import Optional
from pydantic import BaseModel, root_validator


class WalkerOut(BaseModel):
    id: int
    rating: int
    counter: int
    price_per_hour: int
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
    min_dog_size_in_kg: Optional[int]
    max_dog_size_in_kg: Optional[int]
    min_dog_age_in_years: Optional[int]
    max_dog_age_in_years: Optional[int]
    schedule: Optional[str]
    about_walker: Optional[str]

    @root_validator
    def dog_size_check(cls, values):
        if 'min_dog_size_in_kg' in values and 'max_dog_size_in_kg' in values:
            if 0 < values['min_dog_size_in_kg'] < values['max_dog_size_in_kg']:
                return values
            raise ValueError('Does not match 0 < min < max')
        elif 'min_dog_size_in_kg' not in values and 'max_dog_size_in_kg' not in values:
            return values
        else:
            raise ValueError('Min and max value must be filled or not filled at the same time')

    @root_validator
    def dog_age_check(cls, values):
        if 'min_dog_age_in_years' in values and 'max_dog_age_in_years' in values:
            if 0 < values['min_dog_age_in_years'] < values['max_dog_age_in_years']:
                return values
            raise ValueError('Does not match 0 < min < max')
        elif 'min_dog_age_in_years' not in values and 'max_dog_age_in_years' not in values:
            return values
        else:
            raise ValueError('Min and max value must be filled or not filled at the same time')


class WalkerUpdate(BaseModel):
    rating: int
    price_per_hour: int
    counter: int
    min_dog_size_in_kg: Optional[int]
    max_dog_size_in_kg: Optional[int]
    min_dog_age_in_years: Optional[int]
    max_dog_age_in_years: Optional[int]
    schedule: Optional[str]
    about_walker: Optional[str]

    @root_validator
    def dog_size_check(cls, values):
        if 'min_dog_size_in_kg' in values and 'max_dog_size_in_kg' in values:
            if 0 < values['min_dog_size_in_kg'] < values['max_dog_size_in_kg']:
                return values
            raise ValueError('Does not match 0 < min < max')
        elif 'min_dog_size_in_kg' not in values and 'max_dog_size_in_kg' not in values:
            return values
        else:
            raise ValueError('Min and max value must be filled or not filled at the same time')

    @root_validator
    def dog_age_check(cls, values):
        if 'min_dog_age_in_years' in values and 'max_dog_age_in_years' in values:
            if 0 < values['min_dog_age_in_years'] < values['max_dog_age_in_years']:
                return values
            raise ValueError('Does not match 0 < min < max')
        elif 'min_dog_age_in_years' not in values and 'max_dog_age_in_years' not in values:
            return values
        else:
            raise ValueError('Min and max value must be filled or not filled at the same time')