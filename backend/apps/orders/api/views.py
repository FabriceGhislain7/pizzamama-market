from rest_framework import viewsets, permissions
from apps.orders.models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Required for schema generation
    queryset = Order.objects.all()

    # UUID support in OpenAPI
    lookup_field = "id"
    lookup_value_regex = "[0-9a-f-]{36}"

    def get_queryset(self):
        # Prevent drf-spectacular from evaluating queryset with AnonymousUser
        if getattr(self, "swagger_fake_view", False):
            return self.queryset.none()

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)