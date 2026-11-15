from typing import Optional, List
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, BackgroundTasks, Query

from database.connect.connect import Base, engine, get_db
from functions.download.dataID import download_clean_data_id
from functions.basic import current_date
from functions.download.dataDetails import get_data
from functions.pages.data import movie_pages, movie_page_data, person_page_data
from functions.search.data import search_data
from config import url_movie_ids, url_person_ids, api_key, url_movie_details, url_person_details
from schema.search import SearchSchema


app = FastAPI()

# Tworzenie tabel przy starcie aplikacji
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="MovieCheck API", lifespan=lifespan)



@app.get("/create/movie/id")
def get_array_movie_id(popularity: int | None = 3, start: bool | None = True,  db: Session = Depends(get_db)):
    url_movie={"movie": url_movie_ids.format(date=current_date())}
    print(f"[PARAMS] (start: {start}) (popularity: {popularity})")

    download_clean_data_id(url_movie, db, start, popularity)
    return {"message": "Rozpoczęto pobieranie"}


@app.get("/create/person/id")
def get_array_person_id(popularity: int | None = 2, start: bool | None = True, db: Session = Depends(get_db)):
    url_person={"person": url_person_ids.format(date=current_date())}
    print(f"[PARAMS] (start: {start}) (popularity: {popularity})")

    download_clean_data_id(url_person, db, start, popularity)
    return {"message": "Rozpoczęto pobieranie"}


@app.get("/save/movie/data")
def save_movie_data_to_database(background_tasks: BackgroundTasks, db: Session = Depends(get_db), start: bool | None = True):
    background_tasks.add_task(get_data, db=db, start=start, api_key=api_key, url=url_movie_details)
    
    return {"message": "Rozpoczęto pobieranie"}


@app.get("/save/person/data")
def save_person_data_to_database(background_tasks: BackgroundTasks, db: Session = Depends(get_db), start: bool | None = True):
    background_tasks.add_task(get_data, db=db, start=start, api_key=api_key, url=url_person_details)

    return {"message": "Rozpoczęto pobieranie"}


@app.get("/pages/movie")
@app.get("/filters/movie")
def get_movie_data_for_pages(db: Session = Depends(get_db), page: int = 0, number_per_page: int = 10, genre: str | None = None, decade: int | None = None, year: int | None = None, new: bool | None = False):
    return {"pages": movie_pages(db, page, number_per_page, genre, decade, year, new)}
    

@app.get("/movie/{id}")
def get_choosen_movie_data(id: int, db: Session = Depends(get_db)):
    print(f"[MOVIE]: {id}")
    return {f"movie_{id}": movie_page_data(db, id)}


@app.get("/person/{id}")
def get_choosen_person_data(id: int, db: Session = Depends(get_db)):
    print(f"[PERSON]: {id}")
    return {f"person_{id}": person_page_data(db, id)}


@app.get("/search", response_model=SearchSchema)
def search(q: Optional[str] = Query(None), db: Session = Depends(get_db), page: int = 0, number_per_page: int = 10):
    print(f"[SEARCH]: {q}")
    return search_data(db, q, page, number_per_page)