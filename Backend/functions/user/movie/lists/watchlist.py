from functions.user.movie.lists.list_user import ListUser
from database.model.watchlist import WatchlistModel


class Watchlist(ListUser):
    def __init__(self, db, id_user, id_movie = None, TableModel = WatchlistModel):
        super().__init__(db = db, id_user = id_user, id_movie = id_movie, TableModel = TableModel)