from database.model.movie import MovieModel
from database.model.person import PersonModel

from sqlalchemy import select, func, or_, cast, Text
from sqlalchemy import extract

def search_data(db, quote, page, number_per_page):
    table = MovieModel
    query = select(table)
    movieData = searching_movie(query, quote, table, db, page, number_per_page)

    table = PersonModel
    query = select(table)
    personData = searching_person(query, quote, table, db, page, number_per_page)

    return {"movie": movieData, "person": personData}


def searching_movie(query, quote, table, db, page, number_per_page):
    skip = page * number_per_page
    search_in_db = f"%{quote.strip()}%"

    conditions = [table.title.ilike(search_in_db), table.original_title.ilike(search_in_db), cast(table.genres, Text).ilike(search_in_db)]

    if quote.isdigit():
        conditions.append(extract('year', table.release_date) == int(quote))

    result = query.where(or_(*conditions)).order_by(table.popularity.desc()).offset(skip).limit(number_per_page)
    return db.scalars(result).all()


def searching_person(query, quote, table, db, page, number_per_page):
    skip = page * number_per_page
    search_in_db = f"%{quote.strip()}%"

    conditions = [table.name.ilike(search_in_db)]
    
    if quote.isdigit():
        conditions.append(extract('year', table.birthday) == int(quote))

    result = query.where(or_(*conditions)).order_by(table.popularity.desc()).offset(skip).limit(number_per_page)
    return db.scalars(result).all()
