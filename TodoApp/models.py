from database import Base
from sqlalchemy import Column, Integer, String, Boolean


# tutaj znajdują się modele rekordów jakie będą zapisywane do bazy danych
class Todos(Base):
    __tablename__ = "todos"  # nazwa tabeli

    id = Column(
        Integer, primary_key=True, index=True
    )  # kolumna o nazwie id, jest kluczem podstawowym tej tabeli i ma być indeksowana
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(
        Boolean, default=False
    )  # w bazie zapisane jako 0, dla True jest 1
