from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class MovieShortSearchSchema(BaseModel):
    id: int
    title: str
    release_date: date
    poster_path: Optional[str] = None

    class Config:
        from_attributes = True

class PersonShortSearchSchema(BaseModel):
    id: int
    name: str
    profile_path: Optional[str] = None
    birthday: Optional[date] = None

    class Config:
        from_attributes = True

class SearchSchema(BaseModel):
    movie: List[MovieShortSearchSchema] = []
    person: List[PersonShortSearchSchema] = []