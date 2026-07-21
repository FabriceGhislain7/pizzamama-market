from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_order_confirmation_email(self, order_id):
    try:
        from apps.orders.models import Order
        order = Order.objects.select_related("user").get(id=order_id)
        send_mail(
            subject=f"Ordine {order.order_number} confermato — PizzaMama",
            message=f"Grazie {order.user.username}, il tuo ordine {order.order_number} è confermato.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        logger.info("Order confirmation email sent", extra={"order_id": str(order_id)})
    except Exception as exc:
        logger.error("Email send failed", extra={"order_id": str(order_id), "error": str(exc)})
        raise self.retry(exc=exc, countdown=60)


@shared_task
def notify_kitchen(order_id):
    logger.info("Kitchen notification triggered", extra={"order_id": str(order_id)})


@shared_task
def cleanup_abandoned_carts():
    from django.utils import timezone
    from datetime import timedelta
    from apps.orders.models import Cart

    cutoff = timezone.now() - timedelta(hours=24)
    deleted_count, _ = Cart.objects.filter(
        updated_at__lt=cutoff,
        user__isnull=True,
    ).delete()
    logger.info("Abandoned carts cleaned", extra={"deleted": deleted_count})
