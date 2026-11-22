import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer


load_dotenv()

# KLUCZE I DANE ENV
api_key = os.getenv('KEY')
secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')
access_token_minutes = os.getenv('ACCESS_TOKEN_MINUTES')
refresh_token_days = os.getenv('REFRESH_TOKEN_DAYS')

# ADRESY URL TMDB API
url_movie_details = 'https://api.themoviedb.org/3/movie/{ID}'
url_person_details = 'https://api.themoviedb.org/3/person/{ID}'
url_movie_ids = 'http://files.tmdb.org/p/exports/movie_ids_{date}.json.gz'
url_person_ids = 'https://files.tmdb.org/p/exports/person_ids_{date}.json.gz'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")