from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    phone_number: Optional[str]
    avatar_path: Optional[str]
    client_order_count: int

    walker_id: Optional[int]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    password_conf: str
    name: str
    phone_number: Optional[str]

    @validator('password_conf')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v == values['password']:
            return v
        raise ValueError("Password don't match")


class UserUpdate(BaseModel):
    password: constr(min_length=6)
    password_conf: str
    name: str
    phone_number: Optional[str]
    client_order_count: int = 0

    @validator('password_conf')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v == values['password']:
            return v
        raise ValueError("Password don't match")


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
