from apps.audit.models import AuditLog
from apps.audit.middleware import get_current_request


class AuditService:

    @staticmethod
    def log(user, action_type, instance, changes=None):
        request = get_current_request()

        ip_address = None
        user_agent = None

        if request:
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(",")[0].strip()
            else:
                ip_address = request.META.get("REMOTE_ADDR")
            user_agent = request.META.get("HTTP_USER_AGENT")

        AuditLog.objects.create(
            user=user,
            action_type=action_type,
            model_name=instance.__class__.__name__,
            object_id=str(instance.pk),
            changes=changes,
            ip_address=ip_address,
            user_agent=user_agent,
        )
