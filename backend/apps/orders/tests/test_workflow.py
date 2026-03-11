import pytest
from django.core.exceptions import ValidationError
from apps.orders.models import Order
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
def test_valid_status_transition():
    user = UserFactory()

    order = Order.objects.create(
        user=user,
        order_type="pickup",
        subtotal=10,
        delivery_fee=0,
        tax_amount=0,
        discount_amount=0,
        total_amount=10,
    )

    order.change_status("confirmed")
    order.refresh_from_db()

    assert order.status == "confirmed"
    assert order.confirmed_at is not None


@pytest.mark.django_db
def test_invalid_status_transition():
    user = UserFactory()

    order = Order.objects.create(
        user=user,
        order_type="pickup",
        subtotal=10,
        delivery_fee=0,
        tax_amount=0,
        discount_amount=0,
        total_amount=10,
    )

    with pytest.raises(ValueError):
        order.change_status("delivered")


@pytest.mark.django_db
def test_total_amount_validation():
    user = UserFactory()

    with pytest.raises(ValidationError):
        Order.objects.create(
            user=user,
            order_type="pickup",
            subtotal=10,
            delivery_fee=0,
            tax_amount=0,
            discount_amount=0,
            total_amount=5,
        )