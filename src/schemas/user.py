from pydantic import BaseModel, UUID4, Field, validator
from typing import Optional
from datetime import datetime


class UserLogin(BaseModel):
    login: str
    password: str


class UserBase(BaseModel):
    username: str
    hashed_password: str
    fullname: str
    phone: str
    email: str
    avatar_url: str


class UserEdit(BaseModel):
    username: Optional[str]
    hashed_password: Optional[str]
    fullname: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    avatar_url: Optional[str]


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

    @validator("token")
    def hexlify_token(cls, value):
        return value.hex
