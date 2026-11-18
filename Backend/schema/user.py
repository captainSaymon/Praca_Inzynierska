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

class UsersShortDetailsSchema(BaseModel):
    id: int
    email: str
    nickname: str

class UserCreateDetailsSchema(BaseModel):
    email: str
    nickname: str
    password: str
    birthday: date

class UsersUpdateDetailsSchema(BaseModel):
    email: Optional[int] = None
    nickname: Optional[int] = None
    password: Optional[int] = None
    birthday: Optional[date] = None
    gender: Optional[int] = None
    name: Optional[str] = None