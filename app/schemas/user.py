from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: Optional[str]
    password: Optional[str]
    balance: Optional[int] = None
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    name: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    ...


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
# Pydantic’s orm_mode (which you can see in UserInDBBase) will tell the
# Pydantic model to read the data even if it is not a dict, but an ORM model.


# Additional properties to return via API
class User(UserInDBBase):
    pass

