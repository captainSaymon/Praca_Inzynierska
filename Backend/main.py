from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, BackgroundTasks
from contextlib import asynccontextmanager

from database.connect.connect import Base, engine, get_db
from functions.download.dataID import download_clean_data_id
from functions.basic import current_date
from functions.download.dataDetails import get_data
from functions.pages.movie import movie_pages
from config import url_movie_ids, url_person_ids, api_key, url_movie_details, url_person_details


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
def get_movie_data_for_pages(db: Session = Depends(get_db), page: int = 0, number_per_page: int = 10, genre: str | None = None, decade: int | None = None, year: int | None = None):
    return {"pages": movie_pages(db, page, number_per_page, genre, decade, year)}
    
