
from database.model.movie import MovieModel
from database.model.person import PersonModel

from sqlalchemy import select, func, or_
from sqlalchemy import extract



def movie_pages(db, page, number_per_page, genre: str | None = None, decade: int | None = None, year: int | None = None, new: bool | None = False):
    pages_result = []
    skip = page * number_per_page
    table = MovieModel

    query = select(table)

    # sortowanie po gatunku 
    if genre:
        query = query.where(table.genres.any(genre))

    # sortowanie po dekadzie
    if decade:
        decade_end = decade + (10 - decade%10)
        query = query.where(extract('year', table.release_date).between(decade, decade_end))

    # sortowanie po roku
    if year:
        query = query.where(extract('year', table.release_date) == year)

    if new:
        query = query.order_by(table.release_date.desc())

    pages_result = db.scalars(query.order_by(table.popularity.desc()).offset(skip).limit(number_per_page)).all()

    return pages_result



def page_data(db, id: int, table):
    return db.scalars(select(table).where(table.id == id)).first()


def movie_page_data(db, id: int):
    return page_data(db, id, MovieModel)

    
def person_page_data(db, id: int):
    data = page_data(db, id, PersonModel)
    known_for_data = person_in_movies(db, id)
    glossary = {k: v for k, v in data.__dict__.items() if not k.startswith("_")}
    glossary["known_for"] = known_for_data
    
    return glossary


def person_in_movies(db, id):
    query = select(MovieModel).where(
        or_(
            func.jsonb_path_exists(MovieModel.cast_data['cast'], f'$[*].id ? (@ == {id})'),
            func.jsonb_path_exists(MovieModel.cast_data['crew'], f'$[*].id ? (@ == {id})')
        )
    )

    movies = db.scalars(query).all()

    result = []
    for movie in movies:
        cast_list = movie.cast_data.get("cast", [])
        crew_list = movie.cast_data.get("crew", [])
        
        for member in cast_list:
            if member.get("id") == id:
                result.append({
                    "movie_id": movie.id,
                    "movie_title": getattr(movie, "title", "Brak tytułu"),
                    "character": member.get("character"),
                    "backdrop_path": getattr(movie, "backdrop_path", "Brak plakatu")
                })
        
        for member in crew_list:
            if member.get("id") == id:
                result.append({
                    "movie_id": movie.id,
                    "movie_title": getattr(movie, "title", "Brak tytułu"),
                    "job": member.get("job"),
                    "backdrop_path": getattr(movie, "backdrop_path", "Brak plakatu")
                })
                
    return result