import requests
import gzip
import os

from fastapi import FastAPI
from datetime import datetime


app = FastAPI()

@app.get("/download/data")
def get_all_id():
    date=datetime.now().strftime("%m_%d_%Y")
    movie_url={"movie": f"http://files.tmdb.org/p/exports/movie_ids_{date}.json.gz"}
    person_url={"person": f"https://files.tmdb.org/p/exports/person_ids_{date}.json.gz"}

    URLs = [movie_url, person_url]
    status = True
    dictionary = "ID_data"

    os.makedirs(dictionary, exist_ok=True)

    for url in URLs:
        for key, val in url.items():
            response = requests.get(val)
            
            if response.status_code == 200:
                compres_data = response.content
                decode_json = gzip.decompress(compres_data)
                file_name = f"{key}_id_{date}.json"
                path = os.path.join(dictionary, file_name)

                with open(path, "wb") as file:
                    file.write(decode_json)

                print(f"{key} are download")
            else:
                print(f"{key} get error")
                status=False

    return {"Status": status}