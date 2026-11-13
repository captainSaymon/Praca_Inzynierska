import json
import gzip

from database.model.model import ArrayMovie, ArrayPerson
from functions.tools.cleaningID import CleanerID
from functions.basic import save_data_to_database, send_request, get_max_id




# Pobranie listy id i ich oczyszczenie
def download_clean_data_id(url, db, start, popularity):
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
            data = compres_gzip_to_bytes(response)

            # ID od ktorego pobieramy dane
            start_id = None
            
            if start:
                start_id = get_max_id(db, table)
                print(f"[DATA] MAX ID: {start_id}")

            # czyszczenie danych ID
            cleaned_data = clean_data_by_id(data, key, popularity, start_id)

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




# kompresja pliku gzip do bajtow
def compres_gzip_to_bytes(response):
    compres_data = response.content
    byte_data = gzip.decompress(compres_data)
    return byte_data.decode("utf-8")


# czyszczenie danych po id
def clean_data_by_id(data, key, popularity, start_id):
    cleanerID = CleanerID(data, key, popularity, start_id)
    cleaned_data, count = cleanerID.getResult()
    print(f"[CLEANED] {key} \n{count} elements")
    return cleaned_data


# zapis do bazy
def save_data(field_name, table, data, db):
    ID = data.get("id")
    name = data.get(field_name)
    popularity = data.get("popularity")
    element = {"id": ID, field_name: name, "popularity": popularity}

    save_data_to_database(db, table, element)