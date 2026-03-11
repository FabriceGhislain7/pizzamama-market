import pytest
from rest_framework.test import APIClient
from apps.orders.models import Order
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
def test_change_status_endpoint():
    user = UserFactory()
    client = APIClient()
    client.force_authenticate(user=user)

    order = Order.objects.create(
        user=user,
        order_type="pickup",
        subtotal=10,
        delivery_fee=0,
        tax_amount=0,
        discount_amount=0,
        total_amount=10,
    )

    response = client.post(
        f"/api/v1/orders/{order.id}/change-status/",
        {"status": "confirmed"},
    )

    assert response.status_code == 200