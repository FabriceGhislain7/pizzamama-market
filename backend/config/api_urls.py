"""
Central API routing for version v1.
Keeps routing modular and scalable.
"""

from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# -------------------------------------------------------------------
# API Root
# -------------------------------------------------------------------

@extend_schema(exclude=True)
@api_view(["GET"])
def api_root(request):
    return Response({
        "name": "PizzaMama Market API",
        "version": "v1",
        "status": "active",
    })


urlpatterns = [
    path("", api_root, name="api-root"),

    # Schema & Docs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema")),

    # Authentication (JWT - JSON Web Token)
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Domain APIs
    path("accounts/", include("apps.accounts.api.urls")),
    path("products/", include("apps.products.api.urls")),
    path("orders/", include("apps.orders.api.urls")),
]