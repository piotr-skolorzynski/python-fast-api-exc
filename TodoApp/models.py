from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


# tutaj znajdują się modele rekordów jakie będą zapisywane do bazy danych
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)


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
    owner_id = Column(Integer, ForeignKey("users.id"))
