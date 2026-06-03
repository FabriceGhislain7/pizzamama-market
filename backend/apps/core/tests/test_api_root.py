from rest_framework.test import APIClient


def test_api_root_is_public():
    client = APIClient()

    response = client.get("/api/v1/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "PizzaMama Market API",
        "version": "v1",
        "status": "active",
    }
