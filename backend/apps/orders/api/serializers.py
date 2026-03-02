from rest_framework import serializers
from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = [
            "user",
            "order_number",
            "status",
            "confirmed_at",
            "delivered_at",
            "created_at",
            "updated_at",
        ]


class OrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)