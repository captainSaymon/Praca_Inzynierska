from pydantic import BaseModel
from typing import Optional

    
# Dane o Aktorach/twórcach
class PersonDetailsSchema(BaseModel):
    id: int
    adult: bool
    biography: Optional[str] = None
    birthday: Optional[str] = None
    deathday: Optional[str] = None
    gender: int
    known_for_department: Optional[str] = None
    name: str
    place_of_birth: Optional[str] = None
    profile_path: Optional[str] = None