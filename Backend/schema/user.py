from pydantic import BaseModel
from typing import Optional
from datetime import date

    
# Dane o Użytkowniku
class UsersResponseDetailsSchema(BaseModel):
    id: int
    email: str
    nickname: str
    birthday: date
    gender: Optional[int] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True

class UserRegisterDetailsSchema(BaseModel):
    email: str
    nickname: str
    password: str
    birthday: date

class UserLoginDetailsSchema(BaseModel):
    nickname: str
    password: str

class UserDeleteDetailsSchema(BaseModel):
    password: str


class UsersUpdateDetailsSchema(BaseModel):
    email: Optional[str] = None
    nickname: Optional[str] = None
    password: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[int] = None
    name: Optional[str] = None