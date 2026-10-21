import requests
import gzip
import os

from pathlib import Path
from fastapi import FastAPI
from datetime import datetime
from cleaning.id import CleanerID


app = FastAPI()


@app.get("/creat/dataID")
def get_all_id():
    date=datetime.now().strftime("%m_%d_%Y")

    movie_url={"movie": f"http://files.tmdb.org/p/exports/movie_ids_{date}.json.gz"}
    person_url={"person": f"https://files.tmdb.org/p/exports/person_ids_{date}.json.gz"}
    URLs = [movie_url, person_url]

    dictionary = "ID_data"

    return download_clean_data_id(URLs, dictionary)


def download_clean_data_id(URLs, dictionary):
    error_data = []

    for url in URLs:
        for key, val in url.items():

            # Download gzip file with ID data
            response = requests.get(val, timeout=100)
            
            if response.status_code == 200:
                print(f"DOWNLOAD: {key}")

                # Compresing gzip file to bytes then to string
                compres_data = response.content
                byte_data = gzip.decompress(compres_data)
                data = byte_data.decode("utf-8")

                # Clean data ID
                cleanerID = CleanerID(data, key, 3)
                cleaned_data, count = cleanerID.getResult()
                print(f"CLEANED {key} \n{count} elements")

                file_name = f"{key}_id.json"
                if save_data(file_name, dictionary, cleaned_data):
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

def save_data(file_name, dictionary, data):
    path = os.path.join(dictionary, file_name)
    try:
        os.makedirs(dictionary, exist_ok=True)

        with open(path, "w", encoding="utf-8") as file:
            file.write(data)
        return True
    
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    

@app.post("/save/data")
def save_all_data_to_database():
    pass