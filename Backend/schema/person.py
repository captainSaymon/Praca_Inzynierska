from pydantic import BaseModel
from typing import Optional

    
# Dane o Aktorach/twórcach
class PersonDataSchema(BaseModel):
    adult: bool
    biography: Optional[str] = None
    birthday: Optional[str] = None
    deathday: Optional[str] = None
    gender: int
    id: int
    known_for_department: Optional[str] = None
    name: str
    place_of_birth: str
    profile_path: Optional[str] = None