from pathlib import Path
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url

BASE_DIR = Path('.').resolve()

APP_NAME = 'Anime List'

default_dburl = make_url('sqlite:///' +  str(BASE_DIR / 'animelist.db'))

DATABASE_URL = config('DATABASE_URL', default=default_dburl)

engine = create_engine(DATABASE_URL, echo=False)
