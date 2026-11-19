from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from schema.review import ReviewCreateDetailsSchema, ReviewEditDetailsSchema
from database.model.review import ReviewModel




def create_review(db: Session, data: ReviewCreateDetailsSchema):
    review = search_review(db, data.id_user, data.id_movie, check_duplicate=False)

    # tworzenie recenzji
    new_review = ReviewModel(id_user=data.id_user, id_movie=data.id_movie, text_review=data.text_review)

    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=404, detail="Nie znaleziono wskazanego filmu/uzytkownika")
    
    return new_review


def search_review(db: Session, id_user: int, id_movie: int, check_duplicate: bool = True):
    # sprawdzanie czy dane dwa id sa w bazie
    review = db.get(ReviewModel, (id_user, id_movie))

    if not review and check_duplicate:
        raise HTTPException(status_code=404, detail="Nie ma takiej oceny")
    elif review and not check_duplicate:
        raise HTTPException(status_code=400, detail="Taka ocena istnieje")

    return review


def search_all_review(db: Session, id_user: int):
    # sprawdzanie czy nazwa uzytkwonika jest w bazie
    reviews = db.execute(select(ReviewModel).where((ReviewModel.id_user == id_user))).scalars().all()

    if not reviews:
        raise HTTPException(status_code=404, detail="Użytkownik nie posaida żadnych recenzji")

    return reviews


def edit_review(db: Session, id_user: int, id_movie: int, data: ReviewEditDetailsSchema):
    review = search_review(db, id_user, id_movie)

    review.text_review = data.text_review
    db.commit()
    db.refresh(review)
    return review