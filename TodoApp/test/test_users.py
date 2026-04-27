import pytest
from fastapi.testclient import TestClient
from fastapi import status

from .utils import *  # noqa: F403
from ..routers.users import get_db, get_current_user
from ..main import app


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


def test_return_user(client, setup_db, test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "prezio"
    assert response.json()["email"] == "prezio@email.com"
    assert response.json()["first_name"] == "Krzysztof"
    assert response.json()["last_name"] == "Jarzyna"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "(111)-111-1111"


def test_change_password_success(client, setup_db, test_user):
    response = client.put(
        "/user/password",
        json={"password": "testpassword", "new_password": "newpassword"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(client, setup_db, test_user):
    response = client.put(
        "/user/password",
        json={"password": "wrong_password", "new_password": "newpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_change_phone_number_success(client, setup_db, test_user):
    response = client.put("/user/phonenumber/222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT
