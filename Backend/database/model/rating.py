from sqlalchemy import Column, Integer, ForeignKey
from ..connect.connect import Base

class RatingModel(Base):
    __tablename__ = "rating"
    __table_args__ = {"schema": "moviecheckdatabase"}

    id_user = Column(Integer, ForeignKey("MovieCheckDataBase.users.id", ondelete="CASCADE"), primary_key=True)
    id_movie = Column(Integer, ForeignKey("MovieCheckDataBase.movie.id", ondelete="CASCADE"), primary_key=True)
    gender = Column(Integer, nullable=False)