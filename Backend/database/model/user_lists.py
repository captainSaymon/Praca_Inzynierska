from sqlalchemy import Column, Integer, ForeignKey, Date
from ..connect.connect import Base
from datetime import date

from database.model.movie import MovieModel
from database.model.users import UsersModel


class BaseListModel:
    __tablename__ = "list"
    __table_args__ = {"schema": "moviecheckdatabase"}

    id_user = Column(Integer, ForeignKey("moviecheckdatabase.users.id", ondelete="CASCADE"), primary_key=True)
    id_movie = Column(Integer, ForeignKey("moviecheckdatabase.movie.id", ondelete="CASCADE"), primary_key=True)
    added_date = Column(Date, nullable=False, default=date.today)

class ListModel(BaseListModel, Base):
    __tablename__ = "list"
    __table_args__ = {"schema": "moviecheckdatabase"}