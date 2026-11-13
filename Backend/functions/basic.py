import requests

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.exc import DataError




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
def send_request_with_key(url, key):
    params_api_key = {"api_key": key}
    return send_request(url, params=params_api_key)


# Pobieranie najwiekszego id z bazy danych
def get_max_id(db, table):
    max_id = db.query(func.max(table.id)).scalar()
    if max_id:
        return max_id
    return None


# Sprawdzanie czy istnieje w bazie
def check_existing(db, table, data):
    existing_element = db.query(table).filter(table.id == data.get('id')).first()
    if existing_element:
        return True
    return False


# Zapis danych do bazy danych
def save_data_to_database(db, table, data):
    data_dict = (data.model_dump() if hasattr(data, "model_dump") else dict(data))
    
    if check_existing(db, table, data_dict):
        return False

    try:
        new_element = table(**data_dict)

        db.add(new_element)
        db.commit()
        db.refresh(new_element)
        return True
    
    except DataError as e:
        db.rollback() 
        print(f"[ERROR]: {e}\n {data}")


# szukanie w tabli po id
def search_id(id, db, table):
    return db.query(table).filter(table.id == id).first()
        

# Odczyt tylko jednego elementu pokolej z listy
async def read_element(table, db):
    try:
        data = db.query(table).order_by(table.id).yield_per(500)
        for movie in data:
            yield movie

    finally:
        db.close()
