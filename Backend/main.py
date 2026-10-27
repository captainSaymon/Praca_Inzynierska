import requests
import json
import gzip
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from datetime import datetime

from cleaning.id import CleanerID
from schema.movie import MovieDetailsSchema
from schema.person import PersonDataSchema


app = FastAPI()

load_dotenv()
api_key=os.getenv('KEY')
dictionary = "ID_data"
url_movie_details = 'https://api.themoviedb.org/3/movie/{ID}?language=pl&append_to_response=cast'
url_person_data = 'https://api.themoviedb.org/3/person/{ID}?language=pl'
url_movie_ids = 'http://files.tmdb.org/p/exports/movie_ids_{date}.json.gz'
url_person_ids = 'https://files.tmdb.org/p/exports/person_ids_{date}.json.gz'


@app.get("/create/dataID")
def get_all_id():
    url_movie={"movie": url_movie_ids.format(date=current_date())}
    url_person={"person": url_person_ids.format(date=current_date())}
    URLs = [url_movie, url_person]

    return download_clean_data_id(URLs)


# Pobranie listy id i ich oczyszczenie
def download_clean_data_id(URLs):
    error_data = []

    for url in URLs:
        for key, val in url.items():

            # pobranie pliku gzip z danymi ID
            response = send_request(val)
            
            if response.status_code == 200:
                print(f"DOWNLOAD: {key}")

                # kompresja gzip do formy bitowej potem do tekstu
                compres_data = response.content
                byte_data = gzip.decompress(compres_data)
                data = byte_data.decode("utf-8")

                # czyszczenie danych ID
                cleanerID = CleanerID(data, key, 3)
                cleaned_data, count = cleanerID.getResult()
                print(f"CLEANED {key} \n{count} elements")

                file_name = f"{key}_id.json"
                if save_data(file_name, cleaned_data):
                    print(f"SUCCESS \n{key} are save to: {dictionary}")
                else:
                    print(f"ERROR \n{key} are not save to: {dictionary}")
                    error_data.append(key)
            else:
                print(f"ERROR: {key}")
                error_data.append(key)

    if error_data:
        return {"Status": f"Error with data: {error_data}"}
    else:
        return {"Status": "Done"}

# Zapis danych do wybranego folderu
def save_data(file_name, data):
    path = os.path.join(dictionary, file_name)
    try:
        os.makedirs(dictionary, exist_ok=True)

        with open(path, "w", encoding="utf-8") as file:
            file.write(data)
        return True
    
    except Exception as e:
        print(f"ERROR: {e}")
        return False

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
    

@app.post("/save/movie/data")
def save_all_data_to_database():
    return get_data(file_name="movie_id.json", URL=url_movie_details)

@app.post("/save/person/data")
def save_all_data_to_database():
    return get_data(file_name="person_id.json", URL=url_person_data)

# pobieranie danych o filmach
def get_data(file_name: str, URL):
    file_path = os.path.join(dictionary, file_name)

    for element in read_element(file_path):
        id = element.get("id")
        url_data = URL.format(ID=id)
        response = send_request_with_key(url_data)

        if response.status_code == 200:
            result = response.json()
            if "movie" in file_name.lower():
                return {'data': convert_to_schema_movie(result)}
            elif "person" in file_name.lower():
                return {'data': convert_to_schema_person(result)}
            else:
                return {'ERROR': 'There is no specify data to search'}
        else:
            print(f"ERROR: {url_data}")

        break

    return {"Status": "Done"}

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