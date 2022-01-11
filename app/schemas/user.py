from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: Optional[str]
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


# Additional properties to return via API
class UserInDB(UserInDBBase):
    hashed_password: str


class User(UserInDBBase):
    ...

