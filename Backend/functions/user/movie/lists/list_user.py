from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from schema.user_lists import ListElementSchema
from database.model.user_lists import ListModel



class ListUser:
    def __init__(self, db: Session, TableModel: ListModel, id_user: int, id_movie: int | None = None):
        self.db = db
        self.TableModel = TableModel
        self.id_user = id_user
        self.id_movie = id_movie

    def get_list(self):
        array = self.db.execute(select(self.TableModel).where(self.TableModel.id_user == self.id_user)).scalars().all()

        if not array:
            raise HTTPException(status_code=404, detail="Użytkownik nie posaida żadnych filmów na liście")

        return [ListElementSchema.model_validate(row) for row in array]

    def add_movie(self):
        self.search_movie_in_list()

        # tworzenie oceny
        new_movie = self.TableModel(id_user=self.id_user, id_movie=self.id_movie)

        try:
            self.db.add(new_movie)
            self.db.commit()
            self.db.refresh(new_movie)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=404, detail="Nie znaleziono wskazanego filmu/uzytkownika")

    def delete_movie(self):
        result = self.db.execute(select(self.TableModel).where(self.TableModel.id_user == self.id_user, self.TableModel.id_movie == self.id_movie)).scalars().first()

        if not result:
            raise HTTPException(status_code=404, detail="Film nie istnieje w tej liście")

        self.db.delete(result)
        self.db.commit()    
    
    def search_movie_in_list(self):
        # sprawdzanie czy dane dwa id sa w bazie
        result = self.db.get(self.TableModel, (self.id_user, self.id_movie))

        if result:
            raise HTTPException(status_code=400, detail="Film został już dodany")

        return result