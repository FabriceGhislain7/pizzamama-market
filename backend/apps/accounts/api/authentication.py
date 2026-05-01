import logging

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.throttles import LoginRateThrottle

logger = logging.getLogger(__name__)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "Invalid credentials",
    }

    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except AuthenticationFailed as exc:
            request = self.context.get("request")
            client_ip = request.META.get("REMOTE_ADDR") if request else None
            logger.warning(
                "Failed login attempt",
                extra={"client_ip": client_ip},
            )
            raise AuthenticationFailed("Invalid credentials") from exc


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]
