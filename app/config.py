from pathlib import Path
from decouple import config
from sqlalchemy import create_engine

APP_NAME = 'Anime List'

DATABASE_URL = config('DATABASE_URL')

engine = create_engine(DATABASE_URL, echo=False)
