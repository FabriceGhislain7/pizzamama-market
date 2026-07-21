from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncDay
from django.utils.timezone import now
from apps.orders.models import Order, OrderItem


class SalesQueries:

    @staticmethod
    def today_sales():
        today = now().date()
        return Order.objects.filter(
            created_at__date=today,
            status="delivered",
        ).aggregate(
            total_revenue=Sum("total_amount"),
            total_orders=Count("id"),
            avg_order_value=Avg("total_amount"),
        )

    @staticmethod
    def top_selling_products(limit=5):
        return list(
            OrderItem.objects
            .values("pizza__name")
            .annotate(total_sold=Sum("quantity"))
            .order_by("-total_sold")[:limit]
        )

    @staticmethod
    def weekly_trend():
        return list(
            Order.objects
            .filter(status="delivered")
            .annotate(day=TruncDay("created_at"))
            .values("day")
            .annotate(total=Sum("total_amount"), orders=Count("id"))
            .order_by("day")
        )

    @staticmethod
    def customer_lifetime_value(user):
        result = Order.objects.filter(
            user=user,
            status="delivered",
        ).aggregate(total=Sum("total_amount"), orders=Count("id"))
        return result
