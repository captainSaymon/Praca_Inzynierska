from sqlalchemy import Boolean, Column, Integer, Text, Date
from ..connect.connect import Base

class UserModel(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "moviecheckdatabase"}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, unique=True, index=True, nullable=False)
    nickname = Column(Text, unique=True, index=True, nullable=False)
    password = Column(Text, nullable=False)
    birthday = Column(Date, nullable=False)
    adult = Column(Boolean, nullable=True)
    gender = Column(Integer, nullable=True)
    name = Column(Text, nullable=True)