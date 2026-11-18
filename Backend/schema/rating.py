from pydantic import BaseModel, Field


# Dane o ocenach
class RatingCreateDetailsSchema(BaseModel):
    rate: int = Field(..., ge=1, le=10)

class RatingResponseDetailsSchema(BaseModel):
    id_user: int
    id_movie: int
    rate: int

    class Config:
        from_attributes = True
