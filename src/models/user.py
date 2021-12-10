from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    phone_number: Optional[str]
    avatar_path: Optional[str]
    client_order_count: int
    discount: Optional[int]

    walker_id: Optional[int]

    @validator("discount", always=True)
    def validate_count(cls, value, values):
        if values['client_order_count'] >= 100:
            return 10
        else:
            return values['client_order_count'] // 10

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    name: str
    phone_number: Optional[str]


class UserUpdate(BaseModel):
    password: constr(min_length=6)
    name: str
    phone_number: Optional[str]
    client_order_count: int = 0


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
