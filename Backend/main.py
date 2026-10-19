import requests
import gzip
import os

from pathlib import Path
from fastapi import FastAPI
from datetime import datetime
from cleaning.id import CleanerID

app = FastAPI()


dictionary = "ID_data"


@app.get("/download/data")
def get_all_id():
    date=datetime.now().strftime("%m_%d_%Y")
    movie_url={"movie": f"http://files.tmdb.org/p/exports/movie_ids_{date}.json.gz"}
    person_url={"person": f"https://files.tmdb.org/p/exports/person_ids_{date}.json.gz"}

    URLs = [movie_url, person_url]
    status = True

    os.makedirs(dictionary, exist_ok=True)

    for url in URLs:
        for key, val in url.items():
            response = requests.get(val, timeout=100)
            
            if response.status_code == 200:
                compres_data = response.content
                decode_json = gzip.decompress(compres_data)
                file_name = f"{key}_id.json"
                path = os.path.join(dictionary, file_name)

                with open(path, "wb") as file:
                    file.write(decode_json)

                print(f"{key} are download")
            else:
                print(f"{key} get error")
                status=False

    return {"Status": status}

@app.get("/clean/data")
def remove_some_id():
    folder_path = Path(dictionary)
    result = []

    if folder_path.exists() and folder_path.is_dir():
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                with open(file_path, "r", encoding="utf-8") as file:
                    prefix = file_path.name.split("_")[0]
                    content = file.read()

                    cleanerID = CleanerID(content, prefix, 3)
                    cleaned_data, count = cleanerID.getResult()

                    
                    new_file_name = f"{prefix}_cleaned.json" 
                    new_file_path = folder_path / new_file_name
                    
                    with open(new_file_path, "w", encoding="utf-8") as new_file:
                        new_file.write(cleaned_data)
                    el = f"{prefix}: {count}"
                    result.append(el)
                    print(el)
    else:
        print("Error")

    return result