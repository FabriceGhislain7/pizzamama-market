from django.contrib import admin
from .models import (
    Category,
    Allergen,
    Ingredient,
    PizzaSize,
    Pizza,
    PizzaIngredient,
)


admin.site.register(Category)
admin.site.register(Allergen)
admin.site.register(Ingredient)
admin.site.register(PizzaSize)
admin.site.register(Pizza)
admin.site.register(PizzaIngredient)