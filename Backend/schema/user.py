from pydantic import BaseModel
from typing import Optional

    
# Dane o Użytkowniku
class UserDetailsSchema(BaseModel):
    id: int
    email: str
    nickname: str
    password: str
    birthday: str
    adult: Optional[bool] = None
    gender: Optional[int] = None
    name: Optional[str] = None