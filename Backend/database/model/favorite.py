from database.model.user_lists import BaseListModel
from ..connect.connect import Base


class FavoriteModel(BaseListModel, Base):
    __tablename__ = "favorite"
    __table_args__ = {"schema": "moviecheckdatabase"}