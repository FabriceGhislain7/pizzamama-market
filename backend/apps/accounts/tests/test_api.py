import pytest
from rest_framework.test import APIClient
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
def test_login_returns_tokens():
    UserFactory(username="testuser")
    client = APIClient()

    response = client.post(
        "/api/v1/auth/login/",
        {"username": "testuser", "password": "password123"},
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_failure_returns_generic_error():
    UserFactory(username="testuser")
    client = APIClient()

    response = client.post(
        "/api/v1/auth/login/",
        {"username": "testuser", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.data["detail"] == "Invalid credentials"
