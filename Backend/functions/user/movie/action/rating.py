from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from schema.rating import RatingCreateDetailsSchema
from database.model.rating import RatingModel




def create_rating(db: Session, data: RatingCreateDetailsSchema, id_user: int):
    if not (1 <= data.rate <= 10):
        raise HTTPException(status_code=422, detail="Ocena musi mieścić się w przedziale od 1 do 10")

    search_rating(db, id_user, data.id_movie, check_duplicate=False)

    # tworzenie oceny
    new_rating = RatingModel(id_user=id_user, id_movie=data.id_movie, rate=data.rate)

    try:
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=404, detail="Nie znaleziono wskazanego filmu/uzytkownika")
    
    return new_rating


def search_rating(db: Session, id_user: int, id_movie: int, check_duplicate: bool = True):
    # sprawdzanie czy dane dwa id sa w bazie
    rating = db.get(RatingModel, (id_user, id_movie))

    if not rating and check_duplicate:
        raise HTTPException(status_code=404, detail="Nie ma takiej oceny")
    elif rating and not check_duplicate:
        raise HTTPException(status_code=400, detail="Taka ocena istnieje")

    return rating


def search_all_rating(db: Session, id_user: int):
    # sprawdzanie czy nazwa uzytkwonika jest w bazie
    rates = db.execute(select(RatingModel).where((RatingModel.id_user == id_user))).scalars().all()

    if not rates:
        raise HTTPException(status_code=404, detail="Użytkownik nie posaida żadnych ocen")

    return rates