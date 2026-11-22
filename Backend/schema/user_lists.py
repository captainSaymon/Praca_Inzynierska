from pydantic import BaseModel
from datetime import date


# Element listy
class ListElementSchema(BaseModel):
    id_user: int
    id_movie: int
    added_date: date

    class Config:
        from_attributes = True