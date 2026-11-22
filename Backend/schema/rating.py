from pydantic import BaseModel, Field
from typing import List


# tworzenie oceny
class RatingCreateDetailsSchema(BaseModel):
    id_movie: int
    rate: int

# wynik oceny
class RatingResponseDetailsSchema(BaseModel):
    id_movie: int
    rate: int

    class Config:
        from_attributes = True

# wszystkie oceny
class RatingAllResponseDetailsSchema(BaseModel):
    rates: List[RatingResponseDetailsSchema] = []

    class Config:
        from_attributes = True
