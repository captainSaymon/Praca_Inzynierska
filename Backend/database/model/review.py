from sqlalchemy import Column, Integer, ForeignKey, Text, Date
from ..connect.connect import Base
from datetime import date

class ReviewModel(Base):
    __tablename__ = "review"
    __table_args__ = {"schema": "moviecheckdatabase"}

    id_user = Column(Integer, ForeignKey("MovieCheckDataBase.users.id", ondelete="CASCADE"), primary_key=True)
    id_movie = Column(Integer, ForeignKey("MovieCheckDataBase.movie.id", ondelete="CASCADE"), primary_key=True)
    text_review = Column(Text, nullable=False)
    created_date = Column(Date, nullable=False, default=date.today)
