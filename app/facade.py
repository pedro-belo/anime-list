from config import engine
from models import Anime
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)
session = Session()

def get_status_choices():
    return [(choice.value, choice.name.replace('_', ' ').title()) for choice in Anime.StatusChoices]

def anime_to_dct(anime):

    return {
        'id': anime.id,
        'titulo': anime.titulo,
        'episodio_atual': anime.episodio_atual,
        'total_episodios': anime.total_episodios,
        'status': (anime.status.value, anime.status.name.title())
    }    

def get_list():

    queryset = session.query(Anime).order_by('titulo')
    animes = [anime_to_dct(anime) for anime in queryset]

    return animes

def get_list_by_status(status_id):
    return [anime for anime in get_list() if anime['status'][0] == status_id]

def get(pk):
    anime = session.query(Anime).get(pk)
    return anime_to_dct(anime) if anime else None

def create(titulo, episodio_atual, total_episodios, status_id):

    anime = Anime()
    anime.titulo = titulo
    anime.episodio_atual = episodio_atual
    anime.total_episodios = total_episodios
    anime.status = status_id

    session.add(anime)
    session.commit()

    return anime

def update(pk, titulo, episodio_atual, total_episodios, status_id):
    
    anime = session.query(Anime).get(pk)
    anime.titulo = titulo
    anime.episodio_atual = episodio_atual
    anime.total_episodios = total_episodios
    anime.status = status_id
    session.commit()

def delete(pk):
    anime = session.query(Anime).get(pk)
    session.delete(anime)
    session.commit()
