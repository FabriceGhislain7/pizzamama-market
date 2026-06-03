import pytest
from django.db import connection
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_health_check_returns_ok():
    client = APIClient()

    response = client.get(reverse("health-check"))

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "ok",
    }


def test_health_check_returns_service_unavailable_when_database_is_down(monkeypatch):
    client = APIClient()

    def raise_connection_error():
        raise ConnectionError("database unavailable")

    monkeypatch.setattr(connection, "ensure_connection", raise_connection_error)

    response = client.get(reverse("health-check"))

    assert response.status_code == 503
    assert response.json() == {
        "status": "error",
        "database": "error",
    }
