from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_root_endpoint(client: TestClient) -> None:
    """Test the root endpoint returns correct status."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
