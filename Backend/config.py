import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv('KEY')

url_movie_details = 'https://api.themoviedb.org/3/movie/{ID}'
url_person_data = 'https://api.themoviedb.org/3/person/{ID}'
url_movie_ids = 'http://files.tmdb.org/p/exports/movie_ids_{date}.json.gz'
url_person_ids = 'https://files.tmdb.org/p/exports/person_ids_{date}.json.gz'