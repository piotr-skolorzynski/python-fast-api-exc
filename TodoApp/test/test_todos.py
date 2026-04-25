import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import status

from ..routers.auth import get_current_user
from ..routers.todos import (
    get_db,
)  # ważne żeby była to do nadpisania funkcja z todos które testujemy
from ..database import Base
from ..main import app
from ..models import Todos

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# na początek trzeba stworzyć sobie bazę danych do testowania
SQLALCHEMY_TEST_DATABASE_URL = os.getenv("SQLALCHEMY_TEST_DATABASE_URL")

# silnik bazy danych
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# for tests purposes we have to override get_db function to call test db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# create mocked user to override admin user for tests purpose
def override_get_current_user():
    return {"username": "john", "id": 1, "user_role": "admin"}


# # now we can override dependencies and we instanciate test client and override dependecies
@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield db
    with engine.connect() as connection:  # delete inserted todo during the test
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


# create db session
@pytest.fixture
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_all_authenticated(
    client, setup_db, test_todo
):  # kolejność wywołania fixture ma znaczenie
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data == [
        {
            "title": "Learn to code!",
            "description": "Need to learn everyday!",
            "priority": 5,
            "complete": False,
            "owner_id": 1,
            "id": 1,
        }
    ]


def test_read_one_authenticated(client, setup_db, test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {
        "title": "Learn to code!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False,
        "owner_id": 1,
        "id": 1,
    }


def test_read_one_authenticated_not_found(client, setup_db, test_todo):
    response = client.get("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found."}
