from sqlalchemy import Boolean, Column, Float, Integer, String, Text, Date
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from ..connect.connect import Base

class MovieModel(Base):
  __tablename__ = "movie"
  __table_args__ = {"schema": "moviecheckdatabase"}

  id = Column(Integer, primary_key=True, index=True)
  adult = Column(Boolean, nullable=False, default=False)
  backdrop_path = Column(Text, nullable=True)
  budget = Column(Integer, nullable=True)
  genres = Column(ARRAY(Text), nullable=True)
  homepage = Column(Text, nullable=True)
  origin_country = Column(ARRAY(Text), nullable=True)
  original_title = Column(String(255), nullable=True)
  overview = Column(Text, nullable=True)
  poster_path = Column(Text, nullable=True)
  production_companies = Column(JSONB, nullable=True)
  release_date = Column(Date, nullable=True)
  revenue = Column(Integer, nullable=True)
  runtime = Column(Integer, nullable=True)
  status = Column(String(50), nullable=True)
  title = Column(String(255), nullable=False)
  vote_average = Column(Float, nullable=True)
  vote_count = Column(Integer, nullable=True)
  cast_data = Column(JSONB, nullable=True)