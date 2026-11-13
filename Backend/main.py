from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, BackgroundTasks
from contextlib import asynccontextmanager

from database.connect.connect import Base, engine, get_db
from functions.download.dataID import download_clean_data_id
from functions.basic import current_date
from functions.download.dataDetails import get_data
from config import url_movie_ids, url_person_ids, api_key, url_movie_details, url_person_data


app = FastAPI()

# Tworzenie tabel przy starcie aplikacji
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="MovieCheck API", lifespan=lifespan)



@app.get("/create/movie/id")
def get_all_id(popularity: int | None = 3, start: bool | None = True,  db: Session = Depends(get_db)):
    url_movie={"movie": url_movie_ids.format(date=current_date())}
    print(f"[PARAMS] (start: {start}) (popularity: {popularity})")

    download_clean_data_id(url_movie, db, start, popularity)
    return {"message": "Rozpoczęto pobieranie"}


@app.get("/create/person/id")
def get_all_id(popularity: int | None = 2, start: bool | None = True, db: Session = Depends(get_db)):
    url_person={"person": url_person_ids.format(date=current_date())}
    print(f"[PARAMS] (start: {start}) (popularity: {popularity})")

    download_clean_data_id(url_person, db, start, popularity)
    return {"message": "Rozpoczęto pobieranie"}




@app.get("/save/movie/data")
def save_all_data_to_database(background_tasks: BackgroundTasks, db: Session = Depends(get_db), start: bool | None = True):
    background_tasks.add_task(get_data, db=db, start=start, name="movie", api_key=api_key, url_movie_details=url_movie_details, url_person_data=url_person_data)
    
    return {"message": "Rozpoczęto pobieranie"}



@app.post("/save/person/data")
def save_all_data_to_database(db: Session = Depends(get_db), start: bool | None = True):
    return get_data(db, start, name="person")