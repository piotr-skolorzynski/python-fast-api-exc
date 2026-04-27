from fastapi import status
from fastapi.testclient import TestClient

from .utils import *  # noqa: F403
from ..main import app
from ..routers.admin import get_db, get_current_user
from ..models import Todos


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "john", "id": 1, "user_role": "admin"}


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_admin_read_all_authenticated(client, setup_db, test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "title": "Learn to code!",
            "description": "Need to learn everyday!",
            "priority": 5,
            "complete": False,
            "owner_id": 1,
            "id": 1,
        }
    ]


def test_admin_delete_todo(client, setup_db, test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found(client, setup_db, test_todo):
    response = client.delete("/admin/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found."}
