from sqlalchemy import Column, Integer, String, Numeric, quoted_name
from ..connect.connect import Base

class PrimeDataBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    popularity = Column(Numeric, nullable=False, default=0.00)

class ArrayMovie(PrimeDataBaseModel):
    __tablename__ = quoted_name("arraymovie", True)
    __table_args__ = {"schema": "moviecheckdatabase"}

    original_title = Column(String(100), nullable=False)

class ArrayPerson(PrimeDataBaseModel):
    __tablename__ = quoted_name("arrayperson", True)
    __table_args__ = {"schema": "moviecheckdatabase"}

    name = Column(String(100), nullable=False)