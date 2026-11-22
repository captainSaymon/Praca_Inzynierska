from pydantic import BaseModel, Field
from typing import List
from datetime import date


# tworzenie recenzji
class ReviewCreateDetailsSchema(BaseModel):
    id_movie: int
    text_review: str

# Aktualizacja recenzji
class ReviewEditDetailsSchema(BaseModel):
    text_review: str

# wynik recenzji
class ReviewResponseDetailsSchema(BaseModel):
    id_movie: int
    text_review: str
    created_date: date

    class Config:
        from_attributes = True

# wszystkie recenzje
class ReviewAllResponseDetailsSchema(BaseModel):
    reviews: List[ReviewResponseDetailsSchema] = []

    class Config:
        from_attributes = True
