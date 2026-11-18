from pydantic import BaseModel, Field
from typing import List


# tworzenie oceny
class RatingCreateDetailsSchema(BaseModel):
    id_user: int
    id_movie: int
    rate: int = Field(..., ge=1, le=10)

# wynik oceny
class RatingResponseDetailsSchema(BaseModel):
    rate: int

    class Config:
        from_attributes = True

# wszystkie oceny
class RatingAllResponseDetailsSchema(BaseModel):
    rates: List[RatingResponseDetailsSchema] = []

    class Config:
        from_attributes = True
