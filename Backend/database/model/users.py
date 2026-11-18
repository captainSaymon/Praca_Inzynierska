from sqlalchemy import Column, Integer, Text, Date
from ..connect.connect import Base
from datetime import date

class UsersModel(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "moviecheckdatabase"}

    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True, nullable=False)
    nickname = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    birthday = Column(Date, nullable=False)
    gender = Column(Integer, nullable=True)
    name = Column(Text, nullable=True)

    @property
    def check_is_adult(self):
        current = date.today()
        age = current.year - self.birthday.year - ((current.month, current.day) < (self.birthday.month, self.birthday.day))

        if age >= 18:
            return True
        return False