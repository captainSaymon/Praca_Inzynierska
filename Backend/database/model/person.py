from sqlalchemy import Boolean, Column, Integer, Text, Date
from ..connect.connect import Base

class PersonModel(Base):
    __tablename__ = "person"
    __table_args__ = {"schema": "moviecheckdatabase"}

    id = Column(Integer, primary_key=True, index=True)
    adult = Column(Boolean, nullable=False, default=False)
    biography = Column(Text, nullable=True)
    birthday = Column(Date, nullable=True)
    deathday = Column(Date, nullable=True)
    gender = Column(Integer, nullable=False)
    known_for_department = Column(Text, nullable=True)
    name  = Column(Text, nullable=False)
    place_of_birth  = Column(Text, nullable=True)
    profile_path  = Column(Text, nullable=True)