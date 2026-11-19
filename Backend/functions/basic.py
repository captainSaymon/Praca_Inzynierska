import requests

from datetime import datetime
from sqlalchemy import func, select
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
async def check_existing(db, table, data):
    existing_element = await search_id(data.get('id'), db, table)

    if existing_element:
        return True
    return False


# Zapis danych do bazy danych
async def save_data_to_database(db, table, data):
    data_dict = (data.model_dump() if hasattr(data, "model_dump") else dict(data))
    
    if await check_existing(db, table, data_dict):
        return False

    try:
        new_element = table(**data_dict)

        db.add(new_element)
        db.commit()
        db.refresh(new_element)
        return True
    
    except DataError as e:
        db.rollback() 
        print(f"[ERROR]: {e}")


# szukanie w tabli po id
async def search_id(id, db, table):
    search_id = db.execute(select(table).filter(table.id == id))
    return search_id.scalars().first()
        

# Odczyt tylko jednego elementu pokolej z listy
async def read_element(table, db, sort_by_value = None):
    if sort_by_value:
        value = table.id
    else:
        value = sort_by_value
        
    try:
        data = db.execute(select(table).order_by(value)).scalars().all()
        for el in data:
            yield el

    finally:
        db.close()
