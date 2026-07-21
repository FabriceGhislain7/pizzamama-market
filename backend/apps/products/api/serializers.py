from rest_framework import serializers
from apps.products.models import Pizza, Category, PizzaSize


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class PizzaSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaSize
        fields = ["id", "name", "diameter_cm", "price_multiplier"]


class PizzaSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Pizza
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "short_description",
            "base_price",
            "is_featured",
            "is_active",
            "image",
            "category",
        ]
