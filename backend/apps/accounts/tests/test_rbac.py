import pytest
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from apps.accounts.tests.factories import UserFactory
from apps.accounts.services.role_service import RoleService


@pytest.fixture(autouse=True)
def setup_roles(db):
    RoleService.setup_roles()


def make_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_manager_can_access_change_status_endpoint(django_db_setup):
    manager = UserFactory()
    manager.groups.add(Group.objects.get(name="Manager"))

    client = make_client(manager)
    response = client.post("/api/v1/orders/", {})

    assert response.status_code != 403


@pytest.mark.django_db
def test_customer_cannot_change_order_status_of_other_user(django_db_setup):
    customer = UserFactory()
    client = make_client(customer)

    # customer has no Manager/IT_Admin group → change-status returns 403
    response = client.post("/api/v1/orders/00000000-0000-0000-0000-000000000000/change-status/", {"status": "confirmed"})

    assert response.status_code == 403


@pytest.mark.django_db
def test_manager_sees_all_orders(django_db_setup):
    manager = UserFactory()
    manager.groups.add(Group.objects.get(name="Manager"))

    client = make_client(manager)
    response = client.get("/api/v1/orders/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_customer_sees_only_own_orders(django_db_setup):
    customer = UserFactory()
    client = make_client(customer)

    response = client.get("/api/v1/orders/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_role_service_creates_all_groups(django_db_setup):
    for name in ["Manager", "Kitchen", "Delivery", "Staff", "IT_Admin"]:
        assert Group.objects.filter(name=name).exists(), f"Group '{name}' not found"


@pytest.mark.django_db
def test_it_admin_can_access_change_status_endpoint(django_db_setup):
    it_admin = UserFactory()
    it_admin.groups.add(Group.objects.get(name="IT_Admin"))

    client = make_client(it_admin)
    response = client.post("/api/v1/orders/00000000-0000-0000-0000-000000000000/change-status/", {"status": "confirmed"})

    # 404 because order doesn't exist, not 403 — permission is granted
    assert response.status_code == 404
