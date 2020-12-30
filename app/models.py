from config import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy_utils.types.choice import ChoiceType
import enum

Base = declarative_base()

class Anime(Base):
    
    __tablename__ = 'anime'

    class StatusChoices(enum.Enum):
        desconhecido = 1
        assistindo = 2
        completo = 3
        dropado = 4
        em_espera = 5

    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    episodio_atual = Column(Integer)
    total_episodios = Column(Integer)
    status = Column(ChoiceType(StatusChoices, Integer()))

    def __str__(self):
        return self.titulo

Base.metadata.create_all(engine)
