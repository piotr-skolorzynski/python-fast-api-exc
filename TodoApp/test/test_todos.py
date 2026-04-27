from fastapi import status
from fastapi.testclient import TestClient

from .utils import *  # noqa: F403
from ..main import app
from ..models import Todos
from ..routers.auth import get_current_user
from ..routers.todos import (
    get_db,
)  # ważne żeby była to do nadpisania funkcja z todos które testujemy


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


# now we can override dependencies and we instanciate test client and override dependecies
@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_read_all_authenticated(
    client, setup_db, test_todo
):  # kolejność wywołania fixture ma znaczenie
    response = client.get("/todos")
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
    response = client.get("/todos/todo/1")
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
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found."}


def test_create_todo(client, setup_db, test_todo):
    request_data = {
        "title": "New Todo!",
        "description": "New todo description",
        "priority": 5,
        "complete": False,
    }

    response = client.post("/todos/todo/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(client, setup_db, test_todo):
    request_data = {
        "title": "Change the title of the todo already saved!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get("title")


def test_update_todo_not_found(client, setup_db, test_todo):
    request_data = {
        "title": "Change the title of the todo already saved!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found."}


def test_delete_todo(client, setup_db, test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found(client, setup_db, test_todo):
    response = client.delete("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found."}
