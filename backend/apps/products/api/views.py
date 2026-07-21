from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, permissions
from apps.products.models import Pizza, Category, PizzaSize
from .serializers import PizzaSerializer, CategorySerializer, PizzaSizeSerializer


@method_decorator(cache_page(60 * 5), name="dispatch")
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


@method_decorator(cache_page(60 * 5), name="dispatch")
class PizzaSizeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PizzaSizeSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return PizzaSize.objects.filter(is_active=True).order_by("diameter_cm")


@method_decorator(cache_page(60 * 5), name="dispatch")
class PizzaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PizzaSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["category", "is_featured"]
    search_fields = ["name", "description"]
    ordering_fields = ["base_price", "created_at", "name"]

    def get_queryset(self):
        return (
            Pizza.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related("ingredients")
        )
