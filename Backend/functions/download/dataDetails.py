import asyncio
import httpx

from functions.basic import get_max_id, search_id, read_element, save_data_to_database
from schema.person import PersonDetailsSchema
from schema.movie import MovieDetailsSchema
from database.model.movie import MovieModel
from database.model.person import PersonModel
from database.model.model import ArrayMovie, ArrayPerson




# pobieranie danych o filmach
async def get_data(db, start: bool, api_key, url):
    number_limits: int = 40
    limits = httpx.Limits(max_keepalive_connections=number_limits, max_connections=100)

    async with httpx.AsyncClient(limits=limits, timeout=10.0) as client:
        semaphore = asyncio.Semaphore(number_limits)
        params = {"language": "pl", "api_key": api_key}

        action = None            
        if 'person' in url.lower():
            table_id = ArrayPerson
            table_data = PersonModel
            action = 'person'

        elif '/movie' in url.lower():
            table_id = ArrayMovie
            table_data = MovieModel
            action = 'movie'
            params["append_to_response"] = "cast"

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

            url_data = url.format(ID=id)

            task = asyncio.create_task(send_async_request_with_key(client, url_data, semaphore, params))
            tasks.append((id, task))


        for item_id, task in tasks:
            try:
                response = await task

                if response and response.status_code == 200:
                    result = response.json()

                    if action == 'movie':
                        movie_data = convert_to_schema_movie(result)
                        await clean_person_form_list(movie_data, db)
                        await save_data(table_data, movie_data, db)
                    
                    elif action == 'person':
                        person_data = convert_to_schema_person(result)
                        await save_data(table_data, person_data, db)
                    
                    else:
                        print({'ERROR': 'Nie ma danych do wyszukania'})
                else:
                    status = response.status_code if response else "Brak odpowiedzi"
                    print(f"[WARNING] {item_id}: {status}")
                    
            except Exception as e:
                print(f"[ERROR] {item_id}: {e}")


# Wysłanie zapytania z kluczem API async
async def send_async_request_with_key(client: httpx.AsyncClient, url, semaphore: asyncio.Semaphore, params):
    async with semaphore:
        try:
            params = params
            response = await client.get(url, timeout=100, params=params)

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
async def clean_person_form_list(data: MovieDetailsSchema, db):
    cast = data.cast.cast
    crew = data.cast.crew

    data.cast.cast = await clean_array_by_id(cast, db, ArrayPerson)
    data.cast.crew = await clean_array_by_id(crew, db, ArrayPerson)


# czszczenie listy po id z dostepnej tablicy
async def clean_array_by_id(array, db, table):
    result = []
    for person in array:
        person_id = person.id  
        search_result = await search_id(person_id, db, table)
        
        if search_result:
            result.append(person)
            
    return result
    

# konwersja 
def convert_to_schema_movie(data):
    return MovieDetailsSchema.model_validate(data)


# konwersja
def convert_to_schema_person(data):
    return PersonDetailsSchema.model_validate(data)


# zapis danych do bazy
async def save_data(table, data, db):
    kwargs = (data.model_dump() if hasattr(data, "model_dump") else data.dict())

    if "cast" in kwargs:
        kwargs["cast_data"] = kwargs.pop("cast")

    await save_data_to_database(db, table, kwargs)

