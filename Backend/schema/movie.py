from pydantic import BaseModel, field_validator, Field
from typing import List, Optional, Any

# Dane o gatunkach
class Genre(BaseModel):
    name: str

class ProductionCompanies(BaseModel):
    logo_path: Optional[str] = None
    name: str

class CrewMemberSchema(BaseModel):
    id: int
    name: str
    character: Optional[str] = None
    profile_path: Optional[str] = None
    known_for_department: Optional[str] = None
    job: Optional[str] = None

class CreditsSchema(BaseModel):
    cast: List[CrewMemberSchema] = []
    crew: List[CrewMemberSchema] = []
    
# Dane o filmach
class MovieDetailsSchema(BaseModel):
    adult: bool
    backdrop_path: Optional[str] = None
    budget: int
    genres: List[str] = []
    homepage: Optional[str] = None
    id: int
    origin_country: List[str]
    original_title: Optional[str] = None
    overview: Optional[str] = None
    popularity: float = None
    poster_path: Optional[str] = None
    production_companies: List[ProductionCompanies]
    release_date: str
    revenue: Optional[int] = None
    runtime: Optional[int] = None
    status: Optional[str] = None
    title: str
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    cast: CreditsSchema = Field(default_factory=CreditsSchema, alias="credits")

    class Config:
        populate_by_name = True

    @field_validator('genres', mode='before')
    @classmethod
    def convert_to_list(cls, array: Any):
        if isinstance(array, list):
            return [item.get('name') if isinstance(item, dict) else str(item) for item in array]
        return array
