
from database.model.movie import MovieModel
from sqlalchemy import extract



def movie_pages(db, page, number_per_page, genre: str | None = None, decade: int | None = None, year: int | None = None, new: bool | None = False):
    pages_result = []
    skip = page * number_per_page
    table = MovieModel

    query = db.query(table)

    # sortowanie po gatunku 
    if genre:
        query = query.filter(table.genres.any(genre))

    # sortowanie po dekadzie
    if decade:
        decade_end = decade + (10 - decade%10)
        query = query.filter(extract('year', table.release_date).between(decade, decade_end))

    # sortowanie po roku
    if year:
        query = query.filter(extract('year', table.release_date) == year)

    if new:
        query = query.order_by(table.release_date.desc())

    pages_result = query.order_by(table.popularity.desc()).offset(skip).limit(number_per_page).all()

    return pages_result