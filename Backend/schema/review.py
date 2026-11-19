from pydantic import BaseModel, Field
from typing import List


# tworzenie recenzji
class ReviewCreateDetailsSchema(BaseModel):
    id_user: int
    id_movie: int
    text_review: str

# Aktualizacja recenzji
class ReviewEditDetailsSchema(BaseModel):
    text_review: str

# wynik recenzji
class ReviewResponseDetailsSchema(BaseModel):
    text_review: str

    class Config:
        from_attributes = True

# wszystkie recenzje
class ReviewAllResponseDetailsSchema(BaseModel):
    reviews: List[ReviewResponseDetailsSchema] = []

    class Config:
        from_attributes = True
