import requests
import json
import gzip
import os

from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from sqlalchemy.exc import DataError
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from tools.cleaningID import CleanerID
from tools.searchingID import SearcherID
from schema.person import PersonDataSchema
from schema.movie import MovieDetailsSchema
from database.model.model import ArrayMovie, ArrayPerson
from database.connect.connect import Base, engine, get_db


app = FastAPI()

load_dotenv()
api_key=os.getenv('KEY')

url_movie_details = 'https://api.themoviedb.org/3/movie/{ID}?language=pl&append_to_response=cast'
url_person_data = 'https://api.themoviedb.org/3/person/{ID}?language=pl'
url_movie_ids = 'http://files.tmdb.org/p/exports/movie_ids_{date}.json.gz'
url_person_ids = 'https://files.tmdb.org/p/exports/person_ids_{date}.json.gz'

# Tworzenie tabel przy starcie aplikacji
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="MovieCheck API", lifespan=lifespan)



@app.get("/create/dataID")
def get_all_id(popularity: int | None = 3, start: bool | None = True, table: str | None = None,  db: Session = Depends(get_db)):
    url_movie, url_person = {'0': None}, {'0': None}

    if not table or table == 'movie':
        url_movie={"movie": url_movie_ids.format(date=current_date())}
    if not table or table == 'person':
        url_person={"person": url_person_ids.format(date=current_date())}

    URLs = [url_movie, url_person]
    print(f"[PARAMS] (start: {start}) (popularity: {popularity}) (table: {'both' if not table else table})")

    return download_clean_data_id(URLs, db, start, popularity)


# Pobranie listy id i ich oczyszczenie
def download_clean_data_id(URLs, db, start, popularity):
    error_data = False

    for url in URLs:
        for key, val in url.items():
            if not val:
                continue

            print(f"[START] {key} id list download")
            # Ustawienie nazwy kolumny do zapisu
            if key == 'movie':
                field_name = 'original_title'
                table = ArrayMovie
            else:
                field_name = 'name'
                table = ArrayPerson

            # pobranie pliku gzip z danymi ID
            response = send_request(val)
            
            if response.status_code == 200:
                print(f"[DATA] DOWNLOAD: {key}")

                # kompresja gzip do formy bitowej potem do tekstu
                compres_data = response.content
                byte_data = gzip.decompress(compres_data)
                data = byte_data.decode("utf-8")

                # ID od ktorego pobieramy dane
                start_id = None
                
                if start:
                    start_id = get_max_id(db, table)
                    print(f"[DATA] MAX ID: {start_id}")

                # czyszczenie danych ID
                cleanerID = CleanerID(data, key, popularity, start_id)
                cleaned_data, count = cleanerID.getResult()
                print(f"[CLEANED] {key} \n{count} elements")

                for el_json in cleaned_data.splitlines():
                    el_json = el_json.strip()
                    if not el_json:
                        continue

                    try:
                        json_cleaned_data = json.loads(el_json)
                        save_data(field_name, table, json_cleaned_data, db)

                    except json.JSONDecodeError:
                        print(f"[ERROR] That is not JSON: {el_json}")
            else:
                print(f"[ERROR] {key}")
                error_data = True

    if error_data:
        return {"Status": f"Error with data"}
    else:
        return {"Status": "Done"}

# Zapis danych do wybranego folderu
def save_data(field_name, table, data, db):
    ID = data.get("id")
    name = data.get(field_name)
    popularity = data.get("popularity")

    existing_element = db.query(table).filter(table.id == ID).first()
    if existing_element:
        return False

    kwargs = {"id": ID, field_name: name, "popularity": popularity}

    try:
        new_element = table(**kwargs)

        db.add(new_element)
        db.commit()
        db.refresh(new_element)
        return True
    except DataError as e:
        db.rollback() 
        print(f"[BUG] Pominięto element {ID} jest za długi: {len(name)}")

# Pobranie obecnej daty
def current_date():
    return datetime.now().strftime("%m_%d_%Y")

# Wysłanie zapytania z możliwymi parametrami
def send_request(url, timeOut=100, params=None):
    response = requests.get(url, timeout=timeOut, params=params)

    # kodowanie na polskie znaki
    response.encoding = 'utf-8'
    return response

# Wysłanie zapytania z kluczem API
def send_request_with_key(url):
    params_api_key = {"api_key": api_key}
    return send_request(url, params=params_api_key)

# Pobieranie najwiekszego id z bazy danych
def get_max_id(db, table):
    max_id = db.query(func.max(table.id)).scalar()
    if max_id:
        return max_id
    return None



@app.get("/save/movie/data")
def save_all_data_to_database():
    return get_data(file_name="movie_id.json", URL=url_movie_details)



@app.post("/save/person/data")
def save_all_data_to_database():
    return get_data(file_name="person_id.json", URL=url_person_data)

# pobieranie danych o filmach
def get_data(file_name: str, URL):
    dictionary = "ID_data"
    file_path = os.path.join(dictionary, file_name)

    result_data = []
    step = 0

    for element in read_element(file_path):
        print(f"ITEM: {file_name} {step}")

        id = element.get("id")
        url_data = URL.format(ID=id)
        response = send_request_with_key(url_data)

        if response.status_code == 200:
            result = response.json()
            if "movie" in file_name.lower():
                movie_data = convert_to_schema_movie(result)
                clean_person_form_list(movie_data, file_name)

                result_data.append(movie_data)
            
            elif "person" in file_name.lower():
                return {'data': convert_to_schema_person(result)}
            else:
                return {'ERROR': 'There is no specify data to search'}
        else:
            print(f"ERROR: {url_data}")

        if step == 3:
            return {'data': result_data}
        step += 1

    return {"Status": "Done"}

def clean_person_form_list(data: MovieDetailsSchema, file_name: str):
    cast = data.cast.cast
    crew = data.cast.crew

    filtered_cast = clean_array_by_id(file_name, cast)
    filtered_crew = clean_array_by_id(file_name, crew)

    data.cast.cast = filtered_cast
    data.cast.crew = filtered_crew

def clean_array_by_id(file_name, array):
    result = []
    for person in array:
        person_id = person.id  
        searcher = SearcherID(file_name, id=person_id)
        
        if searcher.search():
            result.append(person)
            
    return result

        

# Odczyt tylko jednego elementu pokolej z listy (bez zapisu dzięki yield)
def read_element(file_path):
    if not os.path.exists(file_path):
        print(f"ERROR \npath do not exesits: {file_path}")
        return
    
    with open(file_path, "r", encoding="utf-8") as file:
        for index, line in enumerate(file):
            line = line.strip()
            if not line:
                continue

            try:
                item = json.loads(line)
                yield item
            except json.JSONDecodeError:
                print(f"ERROR: reading line {index} in file: {os.path.basename(file_path)}")

def convert_to_schema_movie(data):
    return MovieDetailsSchema.model_validate(data)

def convert_to_schema_person(data):
    return PersonDataSchema.model_validate(data)