from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from apps.core.models import TimeStampedModel


# CATEGORY
class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="children",
    )

    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "products_category"
        ordering = ["sort_order", "name"]

    def clean(self):
        if self.parent and self.parent == self:
            raise ValidationError("A category cannot be its own parent.")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ALLERGEN
class Allergen(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=10)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "products_allergen"
        ordering = ["name"]

    def __str__(self):
        return self.name

# INGREDIENT
class Ingredient(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    cost_per_unit = models.DecimalField(max_digits=6, decimal_places=2)
    price_per_extra = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    stock_quantity = models.PositiveIntegerField(default=0)
    minimum_stock = models.PositiveIntegerField(default=50)

    allergens = models.ManyToManyField(Allergen, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "products_ingredient"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Ingredient.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.minimum_stock

    def __str__(self):
        return self.name

# PIZZA SIZE
class PizzaSize(TimeStampedModel):
    name = models.CharField(max_length=20, unique=True)
    diameter_cm = models.PositiveIntegerField()
    price_multiplier = models.DecimalField(
        max_digits=4, decimal_places=2, default=1
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "products_pizza_size"
        ordering = ["diameter_cm"]

    def __str__(self):
        return f"{self.name} ({self.diameter_cm}cm)"

# PIZZA
class Pizza(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="pizzas",
    )

    description = models.TextField()
    short_description = models.CharField(max_length=200, blank=True)

    base_price = models.DecimalField(max_digits=8, decimal_places=2)

    ingredients = models.ManyToManyField(
        Ingredient,
        through="PizzaIngredient",
    )

    image = models.ImageField(upload_to="pizzas/", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        db_table = "products_pizza"
        ordering = ["-is_featured", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Pizza.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_price_for_size(self, size):
        return self.base_price * size.price_multiplier

    def __str__(self):
        return self.name

# PIZZA INGREDIENT (THROUGH MODEL)
class PizzaIngredient(TimeStampedModel):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    is_removable = models.BooleanField(default=True)

    class Meta:
        db_table = "products_pizza_ingredient"
        constraints = [
            models.UniqueConstraint(
                fields=["pizza", "ingredient"],
                name="unique_pizza_ingredient",
            )
        ]

    def __str__(self):
        return f"{self.pizza} - {self.ingredient}"
