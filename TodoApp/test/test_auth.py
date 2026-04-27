import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from jose import jwt
from datetime import timedelta

from .utils import *  # noqa: F403
from ..routers.auth import (
    get_db,
    authenticate_user,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
    get_current_user,
)
from ..main import app


# for tests purposes we have to override get_db function to call test db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# now we can override dependencies and we instanciate test client and override dependecies
@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_authenticate_user(client, setup_db, test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "testpassword", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existing_user = authenticate_user("WrongUserName", "testpassword", db)
    assert non_existing_user is False

    wrong_password_user = authenticate_user(test_user.username, "WrongPassword", db)
    assert wrong_password_user is False


def test_create_access_token():
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role


# ten test nawali bo natywnie pytest nie wspiera funkcji asynchronicznych
# do tego trzeba użyć biblioteki pytest asyncio
@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": "testuser", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {"username": "testuser", "id": 1, "user_role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not validate user."
