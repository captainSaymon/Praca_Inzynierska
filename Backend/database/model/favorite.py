from sqlalchemy import Column, Integer, ForeignKey
from ..connect.connect import Base

from database.model.movie import MovieModel
from database.model.users import UsersModel



class FavoriteModel(Base):
    __tablename__ = "favorite"
    __table_args__ = {"schema": "moviecheckdatabase"}

    id_user = Column(Integer, ForeignKey("moviecheckdatabase.users.id", ondelete="CASCADE"), primary_key=True)
    id_movie = Column(Integer, ForeignKey("moviecheckdatabase.movie.id", ondelete="CASCADE"), primary_key=True)