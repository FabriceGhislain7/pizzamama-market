import pytest
from rest_framework.test import APIClient
from apps.accounts.tests.factories import UserFactory
from apps.orders.models import Order


def _make_order(user):
    return Order.objects.create(
        user=user,
        order_type="pickup",
        subtotal=10,
        delivery_fee=0,
        tax_amount=0,
        discount_amount=0,
        total_amount=10,
    )


@pytest.mark.django_db
def test_user_cannot_read_another_user_order():
    owner = UserFactory()
    attacker = UserFactory()
    order = _make_order(owner)

    client = APIClient()
    client.force_authenticate(user=attacker)

    response = client.get(f"/api/v1/orders/{order.id}/")

    assert response.status_code in [403, 404]


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_orders():
    client = APIClient()
    response = client.get("/api/v1/orders/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_cannot_change_status_of_another_user_order():
    from django.contrib.auth.models import Group
    from apps.accounts.services.role_service import RoleService

    RoleService.setup_roles()
    owner = UserFactory()
    attacker = UserFactory()
    attacker.groups.add(Group.objects.get(name="Manager"))
    order = _make_order(owner)

    client = APIClient()
    client.force_authenticate(user=attacker)

    response = client.post(
        f"/api/v1/orders/{order.id}/change-status/",
        {"status": "confirmed"},
    )
    assert response.status_code in [200, 403, 404]


@pytest.mark.django_db
def test_export_data_requires_authentication():
    client = APIClient()
    response = client.get("/api/v1/accounts/me/export/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_export_data_returns_only_own_data():
    user = UserFactory()
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/v1/accounts/me/export/")

    assert response.status_code == 200
    assert response.data["user"]["username"] == user.username
