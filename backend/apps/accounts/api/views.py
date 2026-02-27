from rest_framework import viewsets, permissions
from apps.accounts.models import Address
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Needed for schema generation
    queryset = Address.objects.all()

    # UUID support in schema
    lookup_field = "id"
    lookup_value_regex = "[0-9a-f-]{36}"

    def get_queryset(self):
        # Prevent schema generation errors
        if getattr(self, "swagger_fake_view", False):
            return self.queryset.none()

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}