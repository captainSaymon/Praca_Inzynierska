from database.model.user_lists import BaseListModel
from ..connect.connect import Base


class WatchlistModel(BaseListModel, Base):
    __tablename__ = "watchlist"
    __table_args__ = {"schema": "moviecheckdatabase"}