from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.products.models import Pizza, PizzaSize, Ingredient
from apps.accounts.models import Address
from apps.core.models import TimeStampedModel
import uuid

# CART
class Cart(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="carts",
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        db_table = "orders_cart"
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(user__isnull=False),
                name="unique_active_cart_per_user",
            )
        ]

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return self.user.username if self.user else f"Session {self.session_key}"


# CART ITEM
class CartItem(TimeStampedModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    pizza = models.ForeignKey(Pizza, on_delete=models.PROTECT)
    size = models.ForeignKey(PizzaSize, on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )

    extra_ingredients = models.ManyToManyField(
        Ingredient,
        blank=True,
        related_name="extra_cart_items",
    )

    removed_ingredients = models.ManyToManyField(
        Ingredient,
        blank=True,
        related_name="removed_cart_items",
    )

    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    extra_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        db_table = "orders_cart_item"

    @property
    def subtotal(self):
        return (self.unit_price + self.extra_cost) * self.quantity


# ORDER
class Order(TimeStampedModel):
    STATUS_CHOICES = [
        ("pending", "In Attesa"),
        ("confirmed", "Confermato"),
        ("preparing", "In Preparazione"),
        ("ready", "Pronto"),
        ("out_for_delivery", "In Consegna"),
        ("delivered", "Consegnato"),
        ("cancelled", "Annullato"),
        ("refunded", "Rimborsato"),
    ]

    TYPE_CHOICES = [
        ("delivery", "Consegna"),
        ("pickup", "Ritiro"),
        ("dine_in", "In sede"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order_number = models.CharField(max_length=20, unique=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )

    order_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="delivery",
    )

    delivery_address = models.ForeignKey(
        Address,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    confirmed_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "orders_order"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"PME-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


# ORDER ITEM (SNAPSHOT)
class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    pizza = models.ForeignKey(Pizza, on_delete=models.PROTECT)
    size = models.ForeignKey(PizzaSize, on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    extra_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    extra_ingredients_snapshot = models.JSONField(default=list)
    removed_ingredients_snapshot = models.JSONField(default=list)

    preparation_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "In attesa"),
            ("preparing", "In preparazione"),
            ("ready", "Pronto"),
        ],
        default="pending",
    )

    class Meta:
        db_table = "orders_order_item"

    @property
    def subtotal(self):
        return (self.unit_price + self.extra_cost) * self.quantity


# PAYMENT
class Payment(TimeStampedModel):
    STATUS_CHOICES = [
        ("pending", "In attesa"),
        ("processing", "In elaborazione"),
        ("completed", "Completato"),
        ("failed", "Fallito"),
        ("refunded", "Rimborsato"),
    ]

    METHOD_CHOICES = [
        ("card", "Carta"),
        ("paypal", "PayPal"),
        ("cash", "Contanti"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    transaction_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "orders_payment"


# DELIVERY INFO
class DeliveryInfo(TimeStampedModel):
    STATUS_CHOICES = [
        ("assigned", "Assegnato"),
        ("in_transit", "In transito"),
        ("delivered", "Consegnato"),
        ("failed", "Fallito"),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="delivery_info",
    )

    driver_name = models.CharField(max_length=100, blank=True)
    driver_phone = models.CharField(max_length=17, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    current_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    current_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    customer_rating = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    class Meta:
        db_table = "orders_delivery_info"