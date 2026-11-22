from functions.user.movie.lists.list_user import ListUser
from database.model.favorite import FavoriteModel


class Favorite(ListUser):
    def __init__(self, db, id_user, id_movie = None, TableModel = FavoriteModel):
        super().__init__(db = db, id_user = id_user, id_movie = id_movie, TableModel = TableModel)