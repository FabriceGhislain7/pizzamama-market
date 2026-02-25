from rest_framework import serializers
from apps.products.models import Pizza, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = [
            "id",
            "name",
            "slug",
            "base_price",
            "is_featured",
            "category",
        ]