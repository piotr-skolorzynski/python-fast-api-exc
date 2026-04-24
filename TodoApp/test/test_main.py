from fastapi.testclient import TestClient
from ..main import app
from fastapi import status

client = TestClient(
    app
)  # w main.py znajduje się instancja naszego fastapi o nazwie app


def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}
