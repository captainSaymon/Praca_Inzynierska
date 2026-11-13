import asyncio
import httpx

from functions.basic import get_max_id, search_id, read_element, save_data_to_database
from schema.person import PersonDataSchema
from schema.movie import MovieDetailsSchema
from database.model.movie import MovieModel
from database.model.model import ArrayMovie, ArrayPerson




# pobieranie danych o filmach
async def get_data(db, name: str, start: bool, api_key, url_movie_details, url_person_data):
    number_limits: int = 40
    limits = httpx.Limits(max_keepalive_connections=number_limits, max_connections=100)

    async with httpx.AsyncClient(limits=limits, timeout=10.0) as client:
        semaphore = asyncio.Semaphore(number_limits)

        if name.lower() == 'movie':
            table_id = ArrayMovie
            table_data = MovieModel
            URL=url_movie_details
            
        elif name.lower() == 'person':
            table_id = ArrayPerson
            URL=url_person_data

        else:
            return {"[ERROR]": "zla nazwa"}

        # ID od ktorego pobieramy dane
        start_id = None
        
        if start:
            start_id = get_max_id(db, table_data)
            print(f"[DATA] MAX ID: {start_id}")

        tasks = []

        async for element in read_element(table_id, db):
            id = element.id

            if start_id and start_id > id:
                continue

            url_data = URL.format(ID=id)

            task = asyncio.create_task(send_async_request_with_key(client, url_data, semaphore, api_key))
            tasks.append(task)

            # kontrola tempa
            await asyncio.sleep(1 / number_limits)

            for task in tasks:
                response = await task

                if response and response.status_code == 200:
                    result = response.json()

                    if name.lower() == 'movie':
                        movie_data = convert_to_schema_movie(result)
                        clean_person_form_list(movie_data, db)
                        save_data(MovieModel, movie_data, db)
                    
                    elif name.lower() == 'person':
                        return {'data': convert_to_schema_person(result)}
                    
                    else:
                        return {'ERROR': 'There is no specify data to search'}


# Wysłanie zapytania z kluczem API async
async def send_async_request_with_key(client: httpx.AsyncClient, url, semaphore: asyncio.Semaphore, api_key):
    async with semaphore:
        try:
            params_api_key = {"language": "pl", "append_to_response": "cast", "api_key": api_key}
            response = await client.get(url, timeout=100, params=params_api_key)

            if response.status_code == 200:
                # kodowanie na polskie znaki
                response.encoding = 'utf-8'
                return response
            
            else:
                return None
            
        except Exception as e:
            print(f"Błąd dla ID {url}: {e}")
            return None


# zmniejeszenie ilości aktorów/twórców kierujac sie popularnoscia
def clean_person_form_list(data: MovieDetailsSchema, db):
    cast = data.cast.cast
    crew = data.cast.crew

    data.cast.cast = clean_array_by_id(cast, db, ArrayPerson)
    data.cast.crew = clean_array_by_id(crew, db, ArrayPerson)


# czszczenie listy po id z dostepnej tablicy
def clean_array_by_id(array, db, table):
    result = []
    for person in array:
        person_id = person.id  
        search_result = search_id(person_id, db, table)
        
        if search_result:
            result.append(person)
            
    return result
    

# konwersja 
def convert_to_schema_movie(data):
    return MovieDetailsSchema.model_validate(data)


# konwersja
def convert_to_schema_person(data):
    return PersonDataSchema.model_validate(data)


# zapis danych do bazy
def save_data(table, data, db):
    kwargs = (data.model_dump() if hasattr(data, "model_dump") else data.dict())

    if "cast" in kwargs:
        kwargs["cast_data"] = kwargs.pop("cast")

    save_data_to_database(db, table, kwargs)

