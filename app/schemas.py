from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    password: str
    balance: int


class UserEx(BaseModel):
    username: User

