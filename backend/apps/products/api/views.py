from rest_framework import viewsets, permissions
from apps.products.models import Pizza, Category
from .serializers import PizzaSerializer, CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


class PizzaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PizzaSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["category"]
    search_fields = ["name"]
    ordering_fields = ["base_price", "created_at"]

    def get_queryset(self):
        return (
            Pizza.objects
            .filter(is_active=True)
            .select_related("category")
        )